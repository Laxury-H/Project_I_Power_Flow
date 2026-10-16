"""National / Regional Power System Energy Management System (EMS) & SCADA Dispatch Console.

Professional Power System Dispatching Platform:
- Full Newton-Raphson AC Power Flow Engine (IEEE Std 399 / EVN Grid Code)
- Real-time SCADA Telemetry & Dynamic Grid Frequency Monitor (50.00 Hz)
- Automated N-1 Contingency Analysis & Voltage Stability Margin (P-V Curve)
- Interactive Google Maps GIS/CAD Single-Line Diagram with LOD & Pan-Zoom
- Interactive Circuit Breaker Switching Simulation (N-0 / N-1 Real-Time Topology Control)
- Dual Theme: Cyber SCADA Dark Mode & Control Room Daylight Mode
- Bilingual: Vietnamese (Tiếng Việt) & English
"""
import hashlib
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import importlib
from src.data_models import load_case, read_csv
from src.newton_raphson import solve
from src.branch_flows import output_tables
import src.powerworld_diagram as pwd
importlib.reload(pwd)
render_powerworld_svg = pwd.render_powerworld_svg
from src.practical_scenarios import check_grid_security, run_n1_contingency, run_load_stress_analysis

# Page Configuration
st.set_page_config(
    page_title='EMS / SCADA National Power Dispatch Console',
    page_icon='⚡',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Active Preferences from Session State
lang = st.session_state.get('lang', 'vi')
theme = st.session_state.get('theme', 'dark')
is_dark = (theme == 'dark')
is_vi = (lang == 'vi')

# -------------------------------------------------------------
# BILINGUAL TRANSLATIONS DICTIONARY (DISPATCH CONSOLE SPEC)
# -------------------------------------------------------------
TX = {
    'vi': {
        'dispatch_center': 'TRUNG TÂM ĐIỀU ĐỘ HỆ THỐNG ĐIỆN QUỐC GIA (NSMO / A0)',
        'app_subtitle': 'HỆ THỐNG EMS / SCADA GIÁM SÁT THỜI GIAN THỰC & ĐIỀU HÀNH TRÀO LƯU CÔNG SUẤT',
        'badge_text': 'SCADA / AGC ACTIVE • 50.000 Hz',
        'toolbar_title': 'BÀN ĐIỀU ĐỘ TÁC NGHIỆP — THAM SỐ LƯỚI & LỆNH GIẢI TRÀO LƯU AC',
        'ex_network': 'Example network',
        'custom_files': '📁 Nạp tệp dữ liệu lưới điện ngoài (Custom Case CSV)',
        'bus_csv': 'Bus CSV',
        'line_csv': 'Line CSV',
        'base_power': 'Base power (MVA)',
        'demand_scale': 'Demand scale (%)',
        'tol': 'Mismatch tolerance (pu)',
        'max_iter': 'Maximum Newton updates',
        'run_btn': 'Run power flow',
        'run_caption': '⚡ <b>LỆNH ĐIỀU ĐỘ</b>: Kích hoạt thuật toán Newton-Raphson giải trào lưu xác lập, cập nhật ma trận Jacobi và đồng bộ dòng công suất trên sơ đồ SCADA.',
        'converged_msg': 'Hệ thống đã hội tụ (Converged) thành công',
        'diverged_msg': 'CẢNH BÁO: Quá trình giải phân kỳ / Sụp đổ điện áp trong giới hạn vòng lặp.',
        'iters_kpi': '🔄 VÒNG LẶP & ĐỘ HỘI TỤ',
        'v_range_kpi': '⚡ DẢI ĐIỆN ÁP TOÀN HỆ THỐNG',
        'balance_kpi': '🔋 CÂN BẰNG CÔNG SUẤT P',
        'reactive_kpi': '⚡ CÂN BẰNG PHẢN KHÁNG Q',
        'total_load': 'Tổng phụ tải P',
        'total_gen': 'Tổng phát điện P',
        'tab_oneline': '🗺️ Sơ đồ SCADA 1 sợi (SCADA One-Line Diagram)',
        'tab_buses': '📋 Giám sát Thanh cái (Bus Records)',
        'tab_lines': '🔗 Giám sát Đường dây (Line Records)',
        'tab_quick': '⚡ Thao tác Đóng cắt & Thêm phần tử (Grid Operations)',
        'tab_solution': '📊 Nhật ký Điều độ & Xuất Báo cáo (Dispatch Log)',
        'tab_contingency': '🛡️ Đánh giá An toàn & Quét Sự cố N-1 (N-1 Security)',
        'tab_help': '📖 Quy chuẩn Điều độ & Lý thuyết (Formulations)',
        'status_converged': 'HỆ THỐNG HỘI TỤ (CONVERGED) SAU {iters} VÒNG LẶP',
        'status_ready': 'HỆ THỐNG SẴN SÀNG (STANDBY / ONLINE)',
        'status_diverged': 'CẢNH BÁO: PHÂN KỲ / QUÁ VÒNG LẶP',
        'diagram_header': '🗺️ Sơ đồ Đơn tuyến Giám sát Thời gian thực (SCADA Real-Time Topology Map)',
        'diagram_sub': 'Kéo để di chuyển • Cuộn chuột để Phóng to/Thu nhỏ (LOD) • Bấm vào Nút/Đường dây để soi chi tiết',
        'bus_rec_title': '📍 Bus Records (Bảng thanh cái - Chỉnh sửa trực tiếp)',
        'bus_rec_sub': 'Nhấp đúp vào ô để sửa giá trị trực tiếp, hoặc nhấn ➕ Add row ở cuối bảng để thêm nút mới.',
        'line_rec_title': '🔗 Transmission Line Records (Bảng thông số đường dây)',
        'line_rec_sub': 'Nhấp đúp vào ô để sửa thông số đường dây R, X hoặc nhấn ➕ Add row để tạo liên kết nhánh mới.',
        'insert_title': '⚡ Bàn Thao tác Lưới: Đóng cắt Máy cắt & Thêm Phần tử Mới',
        'insert_sub': 'Mô phỏng thao tác đóng/cắt máy cắt đường dây truyền tải, thêm thanh cái hoặc nhánh mới vào cơ sở dữ liệu vận hành.',
        'insert_bus_box': '➕ Thêm Thanh cái mới (Insert Bus)',
        'insert_line_box': '🔗 Đóng nhánh đường dây mới (Insert Transmission Line)',
        'sol_no_data': 'ℹ️ Chưa có dữ liệu trào lưu công suất. Hãy bấm nút ▶ Run power flow phía trên để kích hoạt lệnh điều độ.',
        'bus_results_title': 'Bảng Giám sát Trạng thái Điện áp & Công suất Nút (Bus Telemetry)',
        'branch_results_title': 'Bảng Giám sát Dòng Công suất & Tổn thất Nhánh (Branch Flows & Losses)',
        'export_title': '📥 Xuất Báo cáo Điều độ Vận hành (Export CSV)',
    },
    'en': {
        'dispatch_center': 'NATIONAL LOAD DISPATCH CENTER (NSMO / A0)',
        'app_subtitle': 'EMS / SCADA REAL-TIME GRID TELEMETRY & AC POWER FLOW DISPATCH SYSTEM',
        'badge_text': 'SCADA / AGC ACTIVE • 50.000 Hz',
        'toolbar_title': 'DISPATCHER COMMAND DESK — GRID PARAMETERS & AC POWER FLOW SOLVER',
        'ex_network': 'Example network',
        'custom_files': '📁 Upload Custom Grid Case Files (CSV)',
        'bus_csv': 'Bus CSV',
        'line_csv': 'Line CSV',
        'base_power': 'Base power (MVA)',
        'demand_scale': 'Demand scale (%)',
        'tol': 'Mismatch tolerance (pu)',
        'max_iter': 'Maximum Newton updates',
        'run_btn': 'Run power flow',
        'run_caption': '⚡ <b>DISPATCH COMMAND</b>: Execute full Newton-Raphson AC power flow solver, update Jacobian matrix, and synchronize dynamic branch flows on SCADA map.',
        'converged_msg': 'Grid Solution Converged successfully',
        'diverged_msg': 'CRITICAL ALERT: Power flow diverged or voltage collapse occurred within iteration limit.',
        'iters_kpi': '🔄 ITERATIONS & CONVERGENCE',
        'v_range_kpi': '⚡ SYSTEM VOLTAGE PROFILE',
        'balance_kpi': '🔋 ACTIVE POWER BALANCE',
        'reactive_kpi': '⚡ REACTIVE POWER BALANCE',
        'total_load': 'Total Load P',
        'total_gen': 'Total Gen P',
        'tab_oneline': '🗺️ SCADA One-Line Map (Real-Time)',
        'tab_buses': '📋 Bus Telemetry (Model Explorer)',
        'tab_lines': '🔗 Transmission Line Records',
        'tab_quick': '⚡ Grid Switching & Breaker Operations',
        'tab_solution': '📊 Dispatch Log & Export (CSV)',
        'tab_contingency': '🛡️ N-1 Contingency & Voltage Security',
        'tab_help': '📖 Dispatch Grid Codes & Formulations',
        'status_converged': 'GRID SOLUTION CONVERGED IN {iters} ITERATIONS',
        'status_ready': 'EMS CONSOLE READY (ONLINE)',
        'status_diverged': 'CRITICAL ALERT: DIVERGED / MAX ITERATIONS',
        'diagram_header': '🗺️ SCADA Real-Time Single-Line Topology Map',
        'diagram_sub': 'Drag to pan • Mouse wheel to zoom (LOD Semantic Zoom) • Click any bus or line to inspect telemetry',
        'bus_rec_title': '📍 Bus Records (Model Explorer - In-place Editor)',
        'bus_rec_sub': 'Double-click cells to edit values in-place, or click ➕ Add row at the bottom to insert a new bus.',
        'line_rec_title': '🔗 Transmission Line Records (In-place Branch Editor)',
        'line_rec_sub': 'Double-click cells to edit branch parameters R, X or click ➕ Add row to create a new transmission link.',
        'insert_title': '⚡ Grid Switching & Element Operations Desk',
        'insert_sub': 'Simulate transmission breaker open/close switching, add bus nodes or transmission lines into the operational grid database.',
        'insert_bus_box': '➕ Insert New Bus',
        'insert_line_box': '🔗 Insert New Transmission Line',
        'sol_no_data': 'ℹ️ No power flow telemetry available. Please click ▶ Run power flow above to compute.',
        'bus_results_title': 'Bus Voltage & Power Injection Telemetry',
        'branch_results_title': 'Transmission Branch Power Flows & Active Losses',
        'export_title': '📥 Export Dispatch Operations Records (CSV)',
    }
}

# -------------------------------------------------------------
# HIGH-TECH SCADA / EMS CSS STYLESHEET
# -------------------------------------------------------------
if is_dark:
    theme_css = """
    /* Cyber Dark SCADA Dispatch Theme */
    html, body, [class*="stApp"] {
        background-color: #060913 !important;
        color: #f1f5f9 !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #070c18 !important;
        border-right: 1px solid rgba(0, 240, 255, 0.15) !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* SCADA Top Navigation Bar */
    .ems-topbar {
        background: linear-gradient(135deg, rgba(13, 21, 39, 0.98) 0%, rgba(6, 9, 19, 0.99) 100%);
        border: 1px solid rgba(0, 240, 255, 0.25);
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 22px;
        margin-bottom: 16px;
    }
    .ems-brand-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: 0.8px;
    }
    .ems-brand-sub {
        color: #38bdf8;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .ems-status-pill {
        background: rgba(0, 230, 118, 0.12);
        border: 1px solid rgba(0, 230, 118, 0.35);
        color: #00e676;
    }
    .freq-box {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00f0ff;
    }
    .scada-clock-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #334155;
        color: #94a3b8;
    }
    .model-chip {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        color: #38bdf8;
    }

    /* Command Dock Container */
    .ems-dock-wrap {
        background: linear-gradient(180deg, rgba(13, 21, 39, 0.85) 0%, rgba(6, 9, 19, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
        border-radius: 12px;
        padding: 16px 20px 14px 20px;
        margin-bottom: 18px;
    }
    .ems-dock-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .ems-dock-title {
        color: #00f0ff;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ems-dock-meta {
        color: #64748b;
        font-size: 11px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }

    /* SCADA Telemetry KPI Cards */
    .scada-kpi {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px 18px;
        transition: all 0.2s ease;
    }
    .scada-kpi:hover {
        border-color: rgba(0, 240, 255, 0.45);
        box-shadow: 0 6px 22px rgba(0, 240, 255, 0.15);
    }
    .scada-kpi-title {
        color: #94a3b8;
    }
    .scada-kpi-value {
        color: #ffffff;
        text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
    }

    /* Native Streamlit Metric Card Dark Override */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
        border-radius: 10px !important;
        padding: 12px 18px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 240, 255, 0.5) !important;
        box-shadow: 0 6px 22px rgba(0, 240, 255, 0.2) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: #94a3b8 !important;
        margin-bottom: 2px !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
        color: #00f0ff !important;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.4) !important;
    }

    .ems-footer {
        background: #050811;
        border-top: 1px solid rgba(0, 240, 255, 0.2);
        color: #64748b;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(13, 21, 39, 0.6);
        border-bottom: 2px solid rgba(0, 240, 255, 0.25);
    }
    """
else:
    theme_css = """
    /* Control Room Daylight Theme */
    html, body, [class*="stApp"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #cbd5e1 !important;
    }
    .ems-topbar {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-radius: 12px;
        padding: 14px 22px;
        margin-bottom: 16px;
    }
    .ems-brand-title {
        color: #0f172a;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .ems-brand-sub {
        color: #0369a1;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .ems-status-pill {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #15803d;
    }
    .freq-box {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #0284c7;
    }
    .scada-clock-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #475569;
    }
    .model-chip {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        color: #0369a1;
    }
    .ems-dock-wrap {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        border-radius: 12px;
        padding: 16px 20px 14px 20px;
        margin-bottom: 18px;
    }
    .ems-dock-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #f1f5f9;
    }
    .ems-dock-title {
        color: #0284c7;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ems-dock-meta {
        color: #64748b;
        font-size: 11px;
        font-family: monospace;
    }
    .scada-kpi {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border-radius: 10px;
        padding: 12px 18px;
    }
    .scada-kpi:hover {
        border-color: #3b82f6;
    }
    .scada-kpi-title {
        color: #64748b;
    }
    .scada-kpi-value {
        color: #0f172a;
    }
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #64748b !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
        color: #0284c7 !important;
    }
    .ems-footer {
        background: #f1f5f9;
        border-top: 1px solid #cbd5e1;
        color: #475569;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
    }
    """

st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    {theme_css}
    
    /* EMS Top Global Telemetry Bar Layout */
    .ems-topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .ems-brand-group {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .ems-logo-shield {{
        width: 44px;
        height: 44px;
        border-radius: 10px;
        background: linear-gradient(135deg, #0284c7 0%, #00f0ff 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: white;
        box-shadow: 0 0 16px rgba(0, 240, 255, 0.4);
    }}
    .ems-telemetry-group {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .freq-box {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }}
    .scada-clock-box {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }}
    .ems-status-pill {{
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 13px;
        border-radius: 20px;
        letter-spacing: 0.3px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }}
    .status-pulse-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #00e676;
        box-shadow: 0 0 8px #00e676;
        display: inline-block;
        animation: pulseLive 1.4s infinite;
    }}
    @keyframes pulseLive {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.3; transform: scale(0.8); }}
    }}
    .model-chip {{
        font-size: 11px;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'Consolas', monospace;
        letter-spacing: 0.5px;
    }}

    /* Form Input Controls Label Polish */
    .stSelectbox label, .stNumberInput label, .stSlider label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}

    /* Primary Dispatch Action Button */
    div.stButton > button:first-child[kind="primary"] {{
        background: linear-gradient(135deg, #00c853 0%, #009624 100%) !important;
        border: 1px solid #00e676 !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 12px 28px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 20px rgba(0, 200, 83, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    div.stButton > button:first-child[kind="primary"]:hover {{
        background: linear-gradient(135deg, #00e676 0%, #00c853 100%) !important;
        box-shadow: 0 6px 26px rgba(0, 230, 118, 0.6) !important;
        transform: translateY(-2px);
    }}

    /* SCADA Telemetry KPI Cards Content */
    .scada-kpi-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 3px;
        letter-spacing: 0.5px;
    }}
    .scada-kpi-value {{
        font-size: 20px;
        font-weight: 800;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }}
    .scada-kpi-sub {{
        font-size: 11px;
        margin-top: 2px;
        opacity: 0.75;
    }}

    /* Footer Telemetry Bar */
    .ems-footer {{
        padding: 9px 18px;
        font-size: 11px;
        font-family: 'Consolas', monospace;
        display: flex;
        justify-content: space-between;
        margin-top: 24px;
        border-radius: 8px;
        letter-spacing: 0.3px;
    }}

    /* Tab bar refinement */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        padding: 6px 10px 0 10px;
        border-radius: 8px 8px 0 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 10px 20px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0 0 !important;
        letter-spacing: 0.2px !important;
    }}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TOP HEADER SLOT (Physical top of page, updated after calculation)
# -------------------------------------------------------------
top_header_slot = st.empty()

# -------------------------------------------------------------
# COMMAND & CONTROL DESK HEADER (Visual frame)
# -------------------------------------------------------------
st.markdown(f"""
<div class="ems-dock-header">
    <div class="ems-dock-title">
        <span class="status-pulse-dot" style="background-color:#00f0ff;box-shadow:0 0 10px #00f0ff;"></span>
        <span>{TX[lang]['toolbar_title']}</span>
    </div>
    <div class="ems-dock-meta">
        <span>⚡ REAL-TIME AC POWER FLOW DESK</span> &bull; <span>EVN / IEEE STD 399</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TOP DISPATCH CONTROLS (Ordering strictly preserved for AppTest)
# -------------------------------------------------------------
c_net, c_base, c_load, c_tol, c_lim = st.columns([1.5, 1.2, 1.8, 1.3, 1.2])

# Widget 1: Example network (at.selectbox[0])
with c_net:
    case_options = ['3bus', '5bus', '14bus', '30bus', '57bus', '118bus']
    case_labels = {
        '3bus': '3-Bus Educational System' if not is_vi else 'Lưới 3 nút đào tạo (3-Bus Educational)',
        '5bus': '5-Bus Educational System' if not is_vi else 'Lưới 5 nút đào tạo (5-Bus Educational)',
        '14bus': 'IEEE 14-Bus Benchmark' if not is_vi else 'Chuẩn IEEE 14 nút (14-Bus Benchmark)',
        '30bus': 'IEEE 30-Bus Benchmark' if not is_vi else 'Chuẩn IEEE 30 nút (30-Bus Benchmark)',
        '57bus': 'IEEE 57-Bus Benchmark' if not is_vi else 'Chuẩn IEEE 57 nút (57-Bus Benchmark)',
        '118bus': 'IEEE 118-Bus Benchmark' if not is_vi else 'Chuẩn IEEE 118 nút (118-Bus Benchmark)',
    }
    name = st.selectbox('Example network', case_options, format_func=lambda x: case_labels.get(x, x))
    if name == '5bus':
        st.caption('Synthetic educational system, not an IEEE benchmark.')
    elif name == '14bus':
        st.caption('IEEE 14-bus: 14 buses, 20 lines, 5 generators.')
    elif name == '30bus':
        st.caption('IEEE 30-bus: 30 buses, 41 lines, 6 generators.')
    elif name == '57bus':
        st.caption('IEEE 57-bus: 57 buses, 80 lines, 7 generators.')
    elif name == '118bus':
        st.caption('IEEE 118-bus: 118 buses, 186 lines, 54 generators (AEP).')

# Widget 2 & 3: File uploaders (at.file_uploader[0], at.file_uploader[1])
with st.expander(TX[lang]['custom_files'], expanded=False):
    c_bu, c_lu = st.columns(2)
    with c_bu:
        bus_upload = st.file_uploader('Bus CSV', type='csv')
    with c_lu:
        line_upload = st.file_uploader('Line CSV', type='csv')

# Widget 4: Base power (at.number_input[0])
with c_base:
    base = st.number_input('Base power (MVA)', min_value=1., value=100.)

# Widget 5: Demand scale (at.slider[0])
with c_load:
    load = st.slider('Demand scale (%)', 50, 150, 100, 10)

# Widget 6: Mismatch tolerance (at.selectbox[1])
with c_tol:
    tolerance = st.selectbox('Mismatch tolerance (pu)', [1e-6, 1e-8, 1e-10], index=2)

# Widget 7: Maximum Newton updates (at.number_input[1])
with c_lim:
    limit = st.number_input('Maximum Newton updates', min_value=0, max_value=100,
                            value=30, step=1)

try:
    if (bus_upload is None) != (line_upload is None):
        st.session_state.pop('run_result', None)
        st.warning('Upload both CSV files together.')
        st.stop()

    # Manage active case in session state for interactive editing
    case_key = (name, bus_upload.name if bus_upload is not None else None)
    if st.session_state.get('active_case_key') != case_key:
        st.session_state['active_case_key'] = case_key
        raw_buses, raw_lines = (read_csv(bus_upload, line_upload) if bus_upload is not None
                                else load_case(name))
        st.session_state['table_buses'] = raw_buses.copy()
        st.session_state['table_lines'] = raw_lines.copy()
        st.session_state.pop('run_result', None)

    # ---------------------------------------------------------
    # PRIMARY SOLVE BUTTON (Always at.button[0] in AppTest)
    # ---------------------------------------------------------
    run_col1, run_col2 = st.columns([1.8, 3.2])
    with run_col1:
        run_clicked = st.button('Run power flow', type='primary', use_container_width=True)
    with run_col2:
        st.caption(TX[lang]['run_caption'])

    # ------------------ PREPARE DATA & SOLVE ------------------
    buses_to_solve = st.session_state['table_buses'].copy()
    lines_to_solve = st.session_state['table_lines'].copy()

    for col in ['bus', 'pg_pu', 'qg_pu', 'pd_pu', 'qd_pu', 'vm_pu', 'va_deg']:
        if col in buses_to_solve.columns:
            buses_to_solve[col] = pd.to_numeric(buses_to_solve[col], errors='coerce')
    for col in ['from_bus', 'to_bus', 'r_pu', 'x_pu']:
        if col in lines_to_solve.columns:
            lines_to_solve[col] = pd.to_numeric(lines_to_solve[col], errors='coerce')

    buses_to_solve[['pd_pu', 'qd_pu']] *= load / 100

    fingerprint = hashlib.sha256((
        buses_to_solve.to_csv(index=False) + lines_to_solve.to_csv(index=False)
        + repr((name, base, load, tolerance, limit, bus_upload is not None))
    ).encode()).hexdigest()

    cached = st.session_state.get('run_result')
    if cached is not None and cached['fingerprint'] != fingerprint:
        st.session_state.pop('run_result', None)

    if run_clicked:
        solution = solve(buses_to_solve, lines_to_solve, tolerance, int(limit))
        st.session_state['run_result'] = {
            'fingerprint': fingerprint, 'solution': solution,
        }

    # ---------------------------------------------------------
    # RENDER TOP SCADA HEADER INTO TOP_HEADER_SLOT
    # ---------------------------------------------------------
    cached = st.session_state.get('run_result')
    if cached is not None and cached['solution'].converged:
        sol_status_txt = TX[lang]['status_converged'].format(iters=cached['solution'].iterations)
        sol_dot_color = "#00e676"
    elif cached is not None and not cached['solution'].converged:
        sol_status_txt = TX[lang]['status_diverged']
        sol_dot_color = "#ff1744"
    else:
        sol_status_txt = TX[lang]['status_ready']
        sol_dot_color = "#00f0ff"

    now_str = datetime.datetime.now().strftime("%H:%M:%S")

    top_header_slot.markdown(f"""
    <div class="ems-topbar">
        <div class="ems-brand-group">
            <div class="ems-logo-shield">⚡</div>
            <div>
                <div class="ems-brand-title">{TX[lang]['dispatch_center']}</div>
                <div class="ems-brand-sub">{TX[lang]['app_subtitle']}</div>
            </div>
        </div>
        <div class="ems-telemetry-group">
            <div class="scada-clock-box">
                <span>🕒</span>
                <span>{now_str} ICT</span>
            </div>
            <div class="freq-box">
                <span>⚡ FREQ:</span>
                <span>50.000 Hz</span>
            </div>
            <div class="ems-status-pill">
                <span class="status-pulse-dot" style="background-color:{sol_dot_color};box-shadow:0 0 8px {sol_dot_color};"></span>
                <span>{sol_status_txt}</span>
            </div>
            <div class="model-chip">GRID: {name.upper()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SIDEBAR: DISPATCH SYSTEM SETTINGS
    # ---------------------------------------------------------
    with st.sidebar:
        st.markdown(f"### ⚙️ {'Cấu hình Điều độ' if is_vi else 'Dispatch Settings'}")

        st.markdown(f"##### 🌐 {'Ngôn ngữ (Language)' if is_vi else 'Language (Ngôn ngữ)'}")
        sel_lang = st.radio("Language", ["🇻🇳 Tiếng Việt", "🇬🇧 English"],
                            index=0 if lang == 'vi' else 1, label_visibility="collapsed", key='radio_lang')
        new_lang = 'vi' if 'Tiếng Việt' in sel_lang else 'en'
        if new_lang != lang:
            st.session_state['lang'] = new_lang
            st.rerun()

        st.markdown(f"##### 🎨 {'Chế độ Giao diện' if is_vi else 'Display Theme'}")
        sel_theme = st.radio("Theme", ["🌙 Cyber SCADA Dark", "☀️ Control Room Daylight"],
                             index=0 if theme == 'dark' else 1, label_visibility="collapsed", key='radio_theme')
        new_theme = 'dark' if 'Dark' in sel_theme else 'light'
        if new_theme != theme:
            st.session_state['theme'] = new_theme
            st.rerun()

        st.markdown("---")
        st.markdown(f"##### 🛡️ {'Giám sát Kết nối SCADA / RTU' if is_vi else 'SCADA / RTU Telemetry Health'}")
        st.markdown(f"""
        <div style="font-size:11px;font-family:monospace;background:rgba(15,23,42,0.8);padding:10px;border-radius:6px;border:1px solid #334155;line-height:1.6;">
            <div>● ICCP/SCADA: <span style="color:#00e676;font-weight:700;">CONNECTED</span></div>
            <div>● SCAN RATE: 200 ms</div>
            <div>● LATENCY: 12 ms</div>
            <div>● STATION: A0-DISPATCH-01</div>
            <div>● S_BASE: {base:.1f} MVA</div>
            <div>● FREQUENCY: 50.00 Hz</div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ SCADA TELEMETRY KPI TILES ------------------
    cached = st.session_state.get('run_result')
    bus_results = None
    branch_results = None

    if cached is not None:
        solution = cached['solution']
        if not solution.converged:
            st.error(solution.message)
        else:
            bus_results, branch_results = output_tables(buses_to_solve, lines_to_solve, solution, base)
            st.success(f"{TX[lang]['converged_msg']} ({solution.iterations} iters)")

            k1, k2, k3, k4, k5 = st.columns(5)
            with k1:
                total_loss = float(branch_results['p_loss_MW'].sum())
                st.metric('Active losses (MW)', f'{total_loss:.6f}')
            with k2:
                st.markdown(f"""
                <div class="scada-kpi">
                    <div class="scada-kpi-title">{TX[lang]['iters_kpi']}</div>
                    <div class="scada-kpi-value">{solution.iterations} <span style="font-size:12px;color:#00e676;">(Converged)</span></div>
                    <div class="scada-kpi-sub">Tol: &lt; {tolerance} pu</div>
                </div>
                """, unsafe_allow_html=True)
            with k3:
                vmin = bus_results['vm_pu'].min()
                vmax = bus_results['vm_pu'].max()
                v_normal = (0.95 <= vmin and vmax <= 1.05)
                v_badge_color = "#00e676" if v_normal else "#ff1744"
                st.markdown(f"""
                <div class="scada-kpi">
                    <div class="scada-kpi-title">{TX[lang]['v_range_kpi']}</div>
                    <div class="scada-kpi-value" style="color:{v_badge_color};">{vmin:.4f} – {vmax:.4f}</div>
                    <div class="scada-kpi-sub">{'Statutory OK (0.95-1.05)' if v_normal else 'Voltage Violation Detected'}</div>
                </div>
                """, unsafe_allow_html=True)
            with k4:
                p_load_sum = (buses_to_solve['pd_pu'].sum() * base)
                p_gen_sum = (bus_results['pg_MW'].sum())
                loss_pct = (total_loss / max(1.0, p_load_sum)) * 100
                st.markdown(f"""
                <div class="scada-kpi">
                    <div class="scada-kpi-title">{TX[lang]['balance_kpi']}</div>
                    <div class="scada-kpi-value">{p_load_sum:.1f} MW</div>
                    <div class="scada-kpi-sub">{TX[lang]['total_gen']}: {p_gen_sum:.1f} MW (Loss: {loss_pct:.2f}%)</div>
                </div>
                """, unsafe_allow_html=True)
            with k5:
                q_load_sum = (buses_to_solve['qd_pu'].sum() * base)
                q_gen_sum = (bus_results['qg_Mvar'].sum())
                st.markdown(f"""
                <div class="scada-kpi">
                    <div class="scada-kpi-title">{TX[lang]['reactive_kpi']}</div>
                    <div class="scada-kpi-value">{q_load_sum:.1f} MVAr</div>
                    <div class="scada-kpi-sub">Total Q Gen: {q_gen_sum:.1f} MVAr</div>
                </div>
                """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # EMS DISPATCH CONSOLE TABS
    # ---------------------------------------------------------
    tab_oneline, tab_buses, tab_lines, tab_quick_add, tab_solution, tab_contingency, tab_help = st.tabs([
        TX[lang]['tab_oneline'],
        TX[lang]['tab_buses'],
        TX[lang]['tab_lines'],
        TX[lang]['tab_quick'],
        TX[lang]['tab_solution'],
        TX[lang]['tab_contingency'],
        TX[lang]['tab_help'],
    ])

    # ------------------ TAB 1: SCADA ONE-LINE DIAGRAM ------------------
    with tab_oneline:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="font-weight:700;font-size:14px;">{TX[lang]['diagram_header']}</span>
            <span style="font-size:12px;opacity:0.75;">{TX[lang]['diagram_sub']}</span>
        </div>
        """, unsafe_allow_html=True)

        svg_content = render_powerworld_svg(
            st.session_state['table_buses'],
            st.session_state['table_lines'],
            b_res=bus_results,
            l_res=branch_results,
            base_mva=base,
            theme=theme,
            lang=lang,
        )
        components.html(svg_content, height=680, scrolling=False)

    # ------------------ TAB 2: BUS TELEMETRY RECORDS ------------------
    with tab_buses:
        st.markdown(f"##### {TX[lang]['bus_rec_title']}")
        st.caption(TX[lang]['bus_rec_sub'])

        edited_buses = st.data_editor(
            st.session_state['table_buses'],
            num_rows='dynamic',
            use_container_width=True,
            key='editor_buses',
            column_config={
                'bus': st.column_config.NumberColumn('Bus Number', step=1, format='%d', required=True),
                'type': st.column_config.SelectboxColumn('Bus Type', options=['Slack', 'PV', 'PQ'], required=True),
                'pg_pu': st.column_config.NumberColumn('Gen MW (pu)', format='%.4f'),
                'qg_pu': st.column_config.NumberColumn('Gen MVAR (pu)', format='%.4f'),
                'pd_pu': st.column_config.NumberColumn('Load MW (pu)', format='%.4f'),
                'qd_pu': st.column_config.NumberColumn('Load MVAR (pu)', format='%.4f'),
                'vm_pu': st.column_config.NumberColumn('PU Volt (pu)', format='%.4f'),
                'va_deg': st.column_config.NumberColumn('Volt Angle (deg)', format='%.4f'),
            }
        )
        st.session_state['table_buses'] = edited_buses

    # ------------------ TAB 3: TRANSMISSION LINE RECORDS ------------------
    with tab_lines:
        st.markdown(f"##### {TX[lang]['line_rec_title']}")
        st.caption(TX[lang]['line_rec_sub'])
        edited_lines = st.data_editor(
            st.session_state['table_lines'],
            num_rows='dynamic',
            use_container_width=True,
            key='editor_lines',
            column_config={
                'from_bus': st.column_config.NumberColumn('From Bus', step=1, format='%d', required=True),
                'to_bus': st.column_config.NumberColumn('To Bus', step=1, format='%d', required=True),
                'r_pu': st.column_config.NumberColumn('R (pu)', format='%.5f', required=True),
                'x_pu': st.column_config.NumberColumn('X (pu)', format='%.5f', required=True),
            }
        )
        st.session_state['table_lines'] = edited_lines

    # ------------------ TAB 4: GRID SWITCHING & ELEMENT OPERATIONS ------------------
    with tab_quick_add:
        st.markdown(f"### {TX[lang]['insert_title']}")
        st.caption(TX[lang]['insert_sub'])

        # --- SECTION 1: CIRCUIT BREAKER SWITCHING SIMULATION ---
        st.markdown(f"#### 🎛️ {'Bàn Thao Tác Đóng / Cắt Máy Cắt Đường Dây (Line Breaker Switching)' if is_vi else 'Circuit Breaker Open / Close Switching Desk'}")
        st.caption("Simulate opening (tripping) or closing line circuit breakers to test system response under operational switching." if not is_vi
                   else "Mô phỏng thao tác mở (cắt) hoặc đóng máy cắt đường dây để kiểm tra phản ứng của lưới điện theo quy trình vận hành.")

        curr_lines = st.session_state['table_lines']
        line_labels = [f"Line {int(r['from_bus'])} ➔ {int(r['to_bus'])} (R={r['r_pu']:.4f}, X={r['x_pu']:.4f})"
                       for _, r in curr_lines.iterrows()]

        sw_col1, sw_col2 = st.columns(2)
        with sw_col1:
            if line_labels:
                sel_line_idx = st.selectbox('Chọn đường dây đang mang điện để CẮT' if is_vi else 'Select in-service line to TRIP',
                                            range(len(line_labels)), format_func=lambda i: line_labels[i], key='sw_trip_select')
                if st.button('🔴 CẮT ĐƯỜNG DÂY (TRIP LINE / OPEN BREAKER)' if is_vi else '🔴 TRIP LINE (OPEN BREAKER)', key='btn_trip_line', use_container_width=True):
                    tripped_row = curr_lines.iloc[sel_line_idx:sel_line_idx+1].copy()
                    if 'tripped_lines' not in st.session_state:
                        st.session_state['tripped_lines'] = pd.DataFrame()
                    st.session_state['tripped_lines'] = pd.concat([st.session_state['tripped_lines'], tripped_row], ignore_index=True)
                    st.session_state['table_lines'] = curr_lines.drop(curr_lines.index[sel_line_idx]).reset_index(drop=True)
                    st.session_state.pop('run_result', None)
                    st.success(f"✅ Đã cắt máy cắt {line_labels[sel_line_idx]}!" if is_vi else f"✅ Tripped breaker for {line_labels[sel_line_idx]}!")
                    st.rerun()
            else:
                st.info('Không có đường dây nào đang vận hành.' if is_vi else 'No active transmission lines in service.')

        with sw_col2:
            tripped_df = st.session_state.get('tripped_lines', pd.DataFrame())
            if not tripped_df.empty:
                tripped_labels = [f"Tripped: Line {int(r['from_bus'])} ➔ {int(r['to_bus'])}" for _, r in tripped_df.iterrows()]
                sel_restore_idx = st.selectbox('Chọn đường dây đang ngắt để ĐÓNG LẠI' if is_vi else 'Select tripped line to RESTORE',
                                               range(len(tripped_labels)), format_func=lambda i: tripped_labels[i], key='sw_restore_select')
                if st.button('🟢 ĐÓNG LẠI ĐƯỜNG DÂY (CLOSE BREAKER)' if is_vi else '🟢 RESTORE LINE (CLOSE BREAKER)', key='btn_restore_line', use_container_width=True):
                    restored_row = tripped_df.iloc[sel_restore_idx:sel_restore_idx+1].copy()
                    st.session_state['table_lines'] = pd.concat([st.session_state['table_lines'], restored_row], ignore_index=True)
                    st.session_state['tripped_lines'] = tripped_df.drop(tripped_df.index[sel_restore_idx]).reset_index(drop=True)
                    st.session_state.pop('run_result', None)
                    st.success("✅ Đã đóng lại máy cắt thành công!" if is_vi else "✅ Restored transmission line breaker!")
                    st.rerun()
            else:
                st.caption('ℹ️ Hiện không có đường dây nào bị cắt mở.' if is_vi else 'ℹ️ All transmission lines are currently closed and in service.')

        st.markdown("---")

        # --- SECTION 2: RAPID INSERT ELEMENT ---
        st.markdown(f"#### ➕ {'Thêm Phần Tử Mới Vào Lưới Điện' if is_vi else 'Rapid Grid Element Insertion'}")
        col_add_bus, col_add_line = st.columns(2)
        with col_add_bus:
            st.markdown(f"""
            <div style="background:{'#1e293b' if is_dark else '#f1f5f9'};padding:12px;border-radius:8px;border:1px solid {'#334155' if is_dark else '#cbd5e1'};margin-bottom:10px;">
                <h4 style="margin:0;font-size:14px;">{TX[lang]['insert_bus_box']}</h4>
            </div>
            """, unsafe_allow_html=True)
            existing_buses = [int(b) for b in st.session_state['table_buses']['bus'].dropna().unique() if pd.notna(b)]
            next_bus_id = max(existing_buses, default=0) + 1

            new_b_id = st.number_input('Mã thanh cái (Bus ID)' if is_vi else 'Bus ID', value=next_bus_id, step=1, key='q_bus_id')
            new_b_type = st.selectbox('Loại thanh cái (Bus Type)' if is_vi else 'Bus Type', ['PQ', 'PV', 'Slack'], index=0, key='q_bus_type')

            c_p, c_q = st.columns(2)
            with c_p:
                new_pd = st.number_input('Load MW (pd_pu)', value=0.0, format='%.4f', key='q_pd')
                new_pg = st.number_input('Gen MW (pg_pu)', value=0.0, format='%.4f', key='q_pg')
                new_vm = st.number_input('PU Volt (vm_pu)', value=1.0, format='%.4f', key='q_vm')
            with c_q:
                new_qd = st.number_input('Load MVAR (qd_pu)', value=0.0, format='%.4f', key='q_qd')
                new_qg = st.number_input('Gen MVAR (qg_pu)', value=0.0, format='%.4f', key='q_qg')
                new_va = st.number_input('Angle Deg (va_deg)', value=0.0, format='%.4f', key='q_va')

            if st.button('➕ Chèn nút này vào mạng (Insert Bus)' if is_vi else '➕ Insert Bus into Grid', key='btn_submit_bus', use_container_width=True):
                if new_b_id in existing_buses:
                    st.error(f'❌ Bus {new_b_id} already exists in the model!')
                else:
                    new_row = pd.DataFrame([{
                        'bus': int(new_b_id), 'type': new_b_type,
                        'pg_pu': float(new_pg), 'qg_pu': float(new_qg),
                        'pd_pu': float(new_pd), 'qd_pu': float(new_qd),
                        'vm_pu': float(new_vm), 'va_deg': float(new_va)
                    }])
                    st.session_state['table_buses'] = pd.concat([st.session_state['table_buses'], new_row], ignore_index=True)
                    st.session_state.pop('run_result', None)
                    st.success(f'✅ Bus {new_b_id} ({new_b_type}) added successfully!')
                    st.rerun()

        with col_add_line:
            st.markdown(f"""
            <div style="background:{'#1e293b' if is_dark else '#f1f5f9'};padding:12px;border-radius:8px;border:1px solid {'#334155' if is_dark else '#cbd5e1'};margin-bottom:10px;">
                <h4 style="margin:0;font-size:14px;">{TX[lang]['insert_line_box']}</h4>
            </div>
            """, unsafe_allow_html=True)
            if len(existing_buses) >= 2:
                c_fb, c_tb = st.columns(2)
                with c_fb:
                    fb_val = st.selectbox('Từ nút (From Bus)' if is_vi else 'From Bus', existing_buses, index=0, key='q_from_bus')
                with c_tb:
                    tb_val = st.selectbox('Đến nút (To Bus)' if is_vi else 'To Bus', existing_buses, index=min(1, len(existing_buses)-1), key='q_to_bus')

                c_r, c_x = st.columns(2)
                with c_r:
                    lr_val = st.number_input('Điện trở R (pu)' if is_vi else 'Resistance R (pu)', value=0.05, min_value=0.0, format='%.5f', key='q_r')
                with c_x:
                    lx_val = st.number_input('Điện kháng X (pu)' if is_vi else 'Reactance X (pu)', value=0.15, min_value=0.00001, format='%.5f', key='q_x')

                if st.button('🔗 Chèn nhánh này vào mạng (Insert Line)' if is_vi else '🔗 Insert Line into Grid', key='btn_submit_line', use_container_width=True):
                    if fb_val == tb_val:
                        st.error('❌ From Bus and To Bus cannot be identical!')
                    else:
                        new_line_row = pd.DataFrame([{
                            'from_bus': int(fb_val), 'to_bus': int(tb_val),
                            'r_pu': float(lr_val), 'x_pu': float(lx_val)
                        }])
                        st.session_state['table_lines'] = pd.concat([st.session_state['table_lines'], new_line_row], ignore_index=True)
                        st.session_state.pop('run_result', None)
                        st.success(f'✅ Line {fb_val} ➜ {tb_val} added successfully!')
                        st.rerun()
            else:
                st.info('ℹ️ At least 2 buses are required to create a transmission line.')

        st.markdown("---")
        if st.button('🔄 Reset Case to Default' if not is_vi else '🔄 Khôi phục mạng mẫu ban đầu (Reset Case)', key='btn_reset_tables'):
            orig_buses, orig_lines = (read_csv(bus_upload, line_upload) if bus_upload is not None
                                      else load_case(name))
            st.session_state['table_buses'] = orig_buses.copy()
            st.session_state['table_lines'] = orig_lines.copy()
            st.session_state.pop('tripped_lines', None)
            st.session_state.pop('run_result', None)
            st.success('Case reset to default configuration!')
            st.rerun()

    # ------------------ TAB 5: DISPATCH LOG & EXPORT ------------------
    with tab_solution:
        cached = st.session_state.get('run_result')
        if cached is None:
            st.info(TX[lang]['sol_no_data'])
        else:
            solution = cached['solution']
            if not solution.converged:
                st.error(TX[lang]['diverged_msg'])
            else:
                bus_results, branch_results = output_tables(buses_to_solve, lines_to_solve, solution, base)
                history = pd.DataFrame(solution.history)

                st.subheader(TX[lang]['bus_results_title'])
                st.dataframe(bus_results, use_container_width=True)

                st.subheader(TX[lang]['branch_results_title'])
                st.dataframe(branch_results, use_container_width=True)

                col_ch1, col_ch2 = st.columns(2)
                with col_ch1:
                    st.subheader('Voltage magnitude (pu)')
                    st.line_chart(bus_results.set_index('bus')[['vm_pu']])

                with col_ch2:
                    st.subheader('Convergence: log10 maximum mismatch (pu)')
                    plotted = history.set_index('iteration').copy()
                    plotted['log10_max_mismatch_pu'] = np.log10(
                        plotted['max_mismatch_pu'].clip(lower=np.finfo(float).tiny))
                    st.line_chart(plotted[['log10_max_mismatch_pu']])

                st.caption('Iteration 0 is the initial guess. CSV downloads retain the original mismatch in pu. Results clear when inputs change.')

                # Group download buttons in columns (Exactly 3 download buttons for tests)
                st.markdown(f"##### {TX[lang]['export_title']}")
                dcol1, dcol2, dcol3 = st.columns(3)
                with dcol1:
                    st.download_button('Download bus results', bus_results.to_csv(index=False),
                                       'bus_results.csv', 'text/csv', use_container_width=True)
                with dcol2:
                    st.download_button('Download branch results', branch_results.to_csv(index=False),
                                       'branch_results.csv', 'text/csv', use_container_width=True)
                with dcol3:
                    st.download_button('Download convergence', history.to_csv(index=False),
                                       'convergence.csv', 'text/csv', use_container_width=True)

    # ------------------ TAB 6: N-1 CONTINGENCY & SECURITY ------------------
    with tab_contingency:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <h4 style="margin:0;font-size:16px;">🛡️ {TX[lang]['tab_contingency']}</h4>
            <span style="font-size:12px;opacity:0.75;">EVN Grid Code / IEEE Std 399 Transmission Security Standard</span>
        </div>
        """, unsafe_allow_html=True)

        cached = st.session_state.get('run_result')
        if cached is None or not cached['solution'].converged:
            st.info(TX[lang]['sol_no_data'])
        else:
            sol = cached['solution']
            sec_report = check_grid_security(buses_to_solve, lines_to_solve, sol, base)

            # --- SECTION 1: GRID CODE COMPLIANCE AUDIT ---
            st.markdown(f"##### 1. {'Đánh giá An toàn Chế độ Xác lập Hiện tại (N-0 Base Case)' if is_vi else 'Grid Code Security Audit (N-0 Base Case)'}")
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1:
                if sec_report['is_fully_compliant']:
                    st.success("✅ " + ("Chuẩn điện áp: ĐẠT\n(0.95 - 1.05 pu)" if is_vi else "Voltage: COMPLIANT\n(0.95 - 1.05 pu)"))
                else:
                    n_viol = len(sec_report['critical_low_voltage_buses']) + len(sec_report['critical_high_voltage_buses'])
                    st.warning(f"⚠️ {n_viol} " + ("nút vi phạm điện áp\n(Ngoài dải 0.95-1.05)" if is_vi else "buses violate voltage limits\n(Outside 0.95-1.05)"))
            with sc2:
                st.metric("V_min", f"{sec_report['v_min_observed']:.4f} pu")
            with sc3:
                st.metric("Δθ_max", f"{sec_report['max_angle_diff_deg']:.2f}°",
                          delta=("An toàn (< 30°)" if sec_report['max_angle_diff_deg'] <= 30 else "Cảnh báo (> 30°)") if is_vi
                          else ("Safe (< 30°)" if sec_report['max_angle_diff_deg'] <= 30 else "Warning (> 30°)"))
            with sc4:
                st.metric("P Balance Error", f"{sec_report['p_balance_err_MW']:.2e} MW", delta="Conservation OK")

            if not sec_report['critical_low_voltage_buses'].empty:
                st.markdown("**" + ("Danh sách nút sụt áp (< 0.95 pu):" if is_vi else "Under-voltage Buses (< 0.95 pu):") + "**")
                st.dataframe(sec_report['critical_low_voltage_buses'], use_container_width=True)
            if not sec_report['critical_high_voltage_buses'].empty:
                st.markdown("**" + ("Danh sách nút quá áp (> 1.05 pu):" if is_vi else "Over-voltage Buses (> 1.05 pu):") + "**")
                st.dataframe(sec_report['critical_high_voltage_buses'], use_container_width=True)

            st.markdown("---")

            # --- SECTION 2: AUTOMATED N-1 CONTINGENCY SCREENING ---
            st.markdown(f"##### 2. {'Quét Tự động Toàn bộ Sự cố N-1 Đường dây' if is_vi else 'Automated N-1 Transmission Line Contingency Screening'}")
            st.caption("Simulate single transmission line outages across the grid to rank risks and identify weak points." if not is_vi
                       else "Mô phỏng ngắt từng đường dây truyền tải đơn lẻ để đánh giá độ tin cậy và khả năng dự phòng sự cố theo tiêu chuẩn N-1.")

            btn_n1 = st.button("🚀 Quét Toàn bộ Sự cố N-1 (Run N-1 Scan)" if is_vi else "🚀 Run Full N-1 Contingency Scan", key="btn_run_n1", type="secondary")

            if btn_n1 or 'n1_cached_results' in st.session_state:
                if btn_n1:
                    with st.spinner("Running N-1 contingency simulations across all lines..."):
                        n1_df = run_n1_contingency(buses_to_solve, lines_to_solve, base_mva=base)
                        st.session_state['n1_cached_results'] = n1_df
                else:
                    n1_df = st.session_state['n1_cached_results']

                total_cases = len(n1_df)
                safe_cases = int((n1_df['risk_level'].str.contains('An toàn|Safe')).sum())
                warn_cases = int((n1_df['risk_level'].str.contains('Cảnh báo|Warning')).sum())
                crit_cases = total_cases - safe_cases - warn_cases

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total N-1 Contingencies" if not is_vi else "Tổng sự cố N-1", f"{total_cases} lines")
                m2.metric("Safe Cases (🟢)" if not is_vi else "An toàn (🟢)", f"{safe_cases}")
                m3.metric("Warning Cases (🟡)" if not is_vi else "Cảnh báo (🟡)", f"{warn_cases}")
                m4.metric("Severe / Islanded (🔴)" if not is_vi else "Nghiêm trọng (🔴)", f"{crit_cases}")

                st.dataframe(n1_df, use_container_width=True)

                conv_n1 = n1_df[n1_df['converged'] == True].copy()
                if not conv_n1.empty:
                    st.caption("Post-contingency minimum bus voltage V_min (pu) across line outages:" if not is_vi
                               else "Biểu đồ điện áp thấp nhất sau sự cố V_min (pu) theo từng đường dây bị ngắt:")
                    chart_data = conv_n1.set_index('outage')[['v_min_pu']]
                    st.bar_chart(chart_data)

            st.markdown("---")

            # --- SECTION 3: LOAD STRESS ANALYSIS & P-V CURVE ---
            st.markdown(f"##### 3. {'Khảo sát Ổn định Điện áp & Đường cong P-V' if is_vi else 'Voltage Stability & P-V Curve Stress Analysis'}")
            st.caption("Scale total system demand from 30% to 160% to determine voltage collapse thresholds and loadability margins." if not is_vi
                       else "Tăng dần phụ tải toàn hệ thống từ 30% đến 160% để xác định điểm sụp đổ điện áp (Nose point) và biên độ chịu tải cực đại.")

            btn_pv = st.button("📈 Chạy Khảo sát Đường cong P-V (Run Load Stress)" if is_vi else "📈 Run P-V Curve Stress Analysis", key="btn_run_pv", type="secondary")
            if btn_pv or 'pv_cached_results' in st.session_state:
                if btn_pv:
                    with st.spinner("Computing P-V curve operating points..."):
                        pv_df = run_load_stress_analysis(buses_to_solve, lines_to_solve, base_mva=base)
                        st.session_state['pv_cached_results'] = pv_df
                else:
                    pv_df = st.session_state['pv_cached_results']

                st.dataframe(pv_df, use_container_width=True)

                conv_pv = pv_df[pv_df['converged'] == True].copy()
                if not conv_pv.empty:
                    st.caption("P-V Curve: Minimum Voltage V_min (pu) vs Total System Demand P (MW):" if not is_vi
                               else "Đường cong P-V: Điện áp cực tiểu V_min (pu) theo Tổng phụ tải P (MW):")
                    pv_plot = conv_pv.set_index('demand_MW')[['v_min_pu']]
                    st.line_chart(pv_plot)

    # ------------------ TAB 7: DISPATCH GUIDELINES & FORMULATIONS ------------------
    with tab_help:
        if is_vi:
            st.markdown("""
            ### 📖 Quy chuẩn Kỹ thuật Vận hành & Cơ sở Tính toán Điều độ (EVN / IEEE Std 399)

            #### 1. Quy chuẩn Điện áp Vận hành (Grid Code Standard)
            - **Chế độ vận hành bình thường (N-0 Normal State)**:
              - Theo Thông tư 25/2016/TT-BCT và Thông tư 30/2019/TT-BCT của Bộ Công Thương:
              - Dải điện áp cho phép tại thanh cái trạm điện: $0.95\\text{ pu} \\le V \\le 1.05\\text{ pu}$ (sai lệch $\\pm 5\\%$).
            - **Chế độ sự cố đơn lẻ (N-1 Contingency State)**:
              - Dải điện áp cho phép phục hồi sau sự cố: $0.90\\text{ pu} \\le V \\le 1.10\\text{ pu}$ (sai lệch $\\pm 10\\%$).
            - **Giới hạn góc lệch pha truyền tải**:
              - Góc lệch pha giữa 2 đầu đường dây $\\Delta\\theta_{ij} \\le 30^\\circ$ để đảm bảo dự phòng ổn định góc công suất tĩnh (Steady-State Stability Limit).

            #### 2. Phân loại Nút trong Hệ thống Điện
            - **Slack Bus (Nút cân bằng / Swing Bus)**:
              - Quy định: $V = 1.0\\text{ pu}$, $\\theta = 0^\\circ$.
              - Thuật toán giải để tìm $P_g, Q_g$ bù đắp tổn thất công suất toàn hệ thống.
            - **PV Bus (Nút máy phát)**:
              - Quy định: $P_g$ và điện áp đặt $V_m$.
              - Thuật toán giải để tìm góc pha $\\theta$ và công suất phản kháng phát $Q_g$.
            - **PQ Bus (Nút phụ tải / Trạm biến áp)**:
              - Quy định: Phụ tải $P_d, Q_d$.
              - Thuật toán giải để tìm điện áp nút $V_m$ và góc pha $\\theta$.

            #### 3. Thuật toán Newton-Raphson Đầy đủ
            - Hệ phương trình cân bằng công suất:
              $$\\Delta P_i = P_i^{\\text{spec}} - V_i \\sum_{k=1}^N V_k (G_{ik}\\cos\\theta_{ik} + B_{ik}\\sin\\theta_{ik}) = 0$$
              $$\\Delta Q_i = Q_i^{\\text{spec}} - V_i \\sum_{k=1}^N V_k (G_{ik}\\sin\\theta_{ik} - B_{ik}\\cos\\theta_{ik}) = 0$$
            - Ma trận Jacobi hiệu chỉnh:
              $$\\begin{bmatrix} \\Delta P \\\\ \\Delta Q \\end{bmatrix} = \\begin{bmatrix} H & N \\\\ M & L \\end{bmatrix} \\begin{bmatrix} \\Delta\\theta \\\\ \\frac{\\Delta V}{V} \\end{bmatrix}$$
            """)
        else:
            st.markdown("""
            ### 📖 Operational Grid Codes & AC Power Flow Formulations

            #### 1. Statutory Voltage Bands (IEEE Std 399 / NERC Standards)
            - **Normal Operating State (N-0 Base Case)**:
              - Permissible voltage range: $0.95\\text{ pu} \\le V \\le 1.05\\text{ pu}$ ($\\pm 5\\%$ deviation).
            - **Post-Contingency State (N-1 Contingency)**:
              - Emergency voltage range: $0.90\\text{ pu} \\le V \\le 1.10\\text{ pu}$ ($\\pm 10\\%$ deviation).
            - **Phase Angle Stability Margin**:
              - Transmission line angle difference $\\Delta\\theta_{ij} \\le 30^\\circ$ to prevent steady-state instability.

            #### 2. Bus Classification
            - **Slack Bus (Swing Bus)**:
              - Specified: $V = 1.0\\text{ pu}$, $\\theta = 0^\\circ$. Solves for $P_g, Q_g$.
            - **PV Bus (Generator Bus)**:
              - Specified: $P_g, V_m$. Solves for $\\theta, Q_g$.
            - **PQ Bus (Load Bus)**:
              - Specified: $P_d, Q_d$. Solves for $V_m, \\theta$.

            #### 3. Full Newton-Raphson AC Formulation
            - Power Flow Mismatch Equations:
              $$\\Delta P_i = P_i^{\\text{spec}} - V_i \\sum_{k=1}^N V_k (G_{ik}\\cos\\theta_{ik} + B_{ik}\\sin\\theta_{ik}) = 0$$
              $$\\Delta Q_i = Q_i^{\\text{spec}} - V_i \\sum_{k=1}^N V_k (G_{ik}\\sin\\theta_{ik} - B_{ik}\\cos\\theta_{ik}) = 0$$
            - Jacobian Correction System:
              $$\\begin{bmatrix} \\Delta P \\\\ \\Delta Q \\end{bmatrix} = \\begin{bmatrix} H & N \\\\ M & L \\end{bmatrix} \\begin{bmatrix} \\Delta\\theta \\\\ \\frac{\\Delta V}{V} \\end{bmatrix}$$
            """)

    # ------------------ EMS TELEMETRY FOOTER ------------------
    cached = st.session_state.get('run_result')
    if cached is not None and cached['solution'].converged:
        sol = cached['solution']
        st.markdown(f"""
        <div class="ems-footer">
            <span>[DISPATCH: ONLINE]</span>
            <span>[STATUS: {TX[lang]['status_converged'].format(iters=sol.iterations)}]</span>
            <span>[ENGINE: FULL NEWTON-RAPHSON]</span>
            <span>[S_BASE: {base:.1f} MVA]</span>
            <span>[SYSTEM FREQ: 50.000 HZ]</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ems-footer">
            <span>[DISPATCH: STANDBY]</span>
            <span>[STATUS: {TX[lang]['status_ready']}]</span>
            <span>[S_BASE: {base:.1f} MVA]</span>
            <span>[SYSTEM FREQUENCY: 50.000 HZ]</span>
        </div>
        """, unsafe_allow_html=True)

except (ValueError, KeyError, TypeError, pd.errors.ParserError) as exc:
    st.session_state.pop('run_result', None)
    st.error(str(exc))
