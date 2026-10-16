"""PowerWorld-style Interactive Vector Single-Line Diagram Engine (SVG + Web GIS Map Viewport).

Features:
- Google Maps-style interactive pan (click & drag) and smooth zoom (mouse wheel / touch pinch / buttons)
- Level of Detail (LOD / Semantic Zoom):
    * Zoom xa (Macro overview): Hiển thị bộ khung lưới, thanh cái và đường dây thông thoáng, không rối mắt
    * Zoom vừa: Hiển thị điện áp (pu, badge xanh/đỏ) và dòng công suất hoạt họa
    * Zoom cận: Hiển thị chi tiết toàn bộ công suất phát (MW/MVAR), phụ tải và tổn thất
- Interactive Click-to-Inspect (Google Maps InfoWindow):
    * Bấm vào bất kỳ nút nào để xem thẻ thông số đầy đủ (Điện áp, góc pha, P phát, P tải, danh sách nhánh nối)
    * Bấm vào bất kỳ nhánh nào để xem dòng công suất, tổn thất, và trở kháng
- Thanh công cụ bản đồ: Nút Phóng to (+), Thu nhỏ (-), Căn vừa màn hình (Fit), và Hộp tìm kiếm nhanh nút (Search Bus)
- Dual Theme: Hỗ trợ Dark Mode & Light Mode
- Bilingual: Hỗ trợ Tiếng Việt & English
"""
import math
import numpy as np
import pandas as pd


def get_bus_layout(bus_ids, lines_df=None):
    """Calculates clean 2D coordinates for buses according to network topology and size."""
    n = len(bus_ids)
    coords = {}

    if n == 3:
        width, height = 1000, 650
        coords[bus_ids[0]] = (250, 180)
        coords[bus_ids[1]] = (750, 180)
        coords[bus_ids[2]] = (500, 480)
        return coords, width, height

    elif n == 5:
        width, height = 1100, 700
        pos = [(550, 130), (920, 280), (780, 560), (320, 560), (180, 280)]
        for i, bid in enumerate(bus_ids):
            coords[bid] = pos[i % len(pos)]
        return coords, width, height

    elif n == 14:
        width, height = 1350, 850
        ieee14_pos = {
            1: (180, 140), 2: (500, 140), 3: (880, 140), 4: (680, 290), 5: (340, 290),
            6: (920, 320), 7: (720, 450), 8: (940, 470), 9: (600, 540), 10: (460, 540),
            11: (320, 540), 12: (180, 460), 13: (180, 560), 14: (640, 660)
        }
        for bid in bus_ids:
            coords[bid] = ieee14_pos.get(bid, (550, 350))
        return coords, width, height

    elif n <= 30:
        # Concentric dual-ring layout for IEEE 30-bus
        width, height = 1800, 1200
        cx, cy = width // 2, height // 2
        inner_count = min(10, n // 3)
        outer_count = n - inner_count
        for i, bid in enumerate(bus_ids[:inner_count]):
            ang = 2 * math.pi * i / inner_count - math.pi / 2
            coords[bid] = (int(cx + 300 * math.cos(ang)), int(cy + 200 * math.sin(ang)))
        for i, bid in enumerate(bus_ids[inner_count:]):
            ang = 2 * math.pi * i / outer_count - math.pi / 2
            coords[bid] = (int(cx + 620 * math.cos(ang)), int(cy + 400 * math.sin(ang)))
        return coords, width, height

    else:
        # Serpentine Electrical Grid Topology for large systems (57-bus, 118-bus, etc.)
        aspect = 1.45
        cols = max(4, int(math.ceil(math.sqrt(n * aspect))))
        rows = int(math.ceil(n / cols))

        spacing_x = 220
        spacing_y = 200
        margin_x = 180
        margin_y = 160

        width = margin_x * 2 + (cols - 1) * spacing_x
        height = margin_y * 2 + (rows - 1) * spacing_y

        for idx, bid in enumerate(bus_ids):
            r = idx // cols
            c_raw = idx % cols
            c = (cols - 1 - c_raw) if (r % 2 == 1) else c_raw
            x = int(margin_x + c * spacing_x)
            y = int(margin_y + r * spacing_y)
            coords[bid] = (x, y)

        return coords, width, height


def render_powerworld_svg(buses_df, lines_df, b_res=None, l_res=None, base_mva=100.0, theme='dark', lang='vi'):
    """Generates an interactive Google Maps-style PowerWorld single-line diagram viewer (HTML/SVG/JS)."""
    buses = buses_df.copy()
    lines = lines_df.copy()

    for col in ['bus', 'pg_pu', 'qg_pu', 'pd_pu', 'qd_pu', 'vm_pu', 'va_deg']:
        if col in buses.columns:
            buses[col] = pd.to_numeric(buses[col], errors='coerce')
    for col in ['from_bus', 'to_bus', 'r_pu', 'x_pu']:
        if col in lines.columns:
            lines[col] = pd.to_numeric(lines[col], errors='coerce')

    bus_ids = [int(b) for b in buses['bus'].dropna().unique()]
    n_buses = len(bus_ids)
    coords, canvas_w, canvas_h = get_bus_layout(bus_ids, lines)

    # Theme tokens
    is_dark = (theme == 'dark')
    bg_style = 'radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%)' if is_dark else '#f8fafc'
    grid_dot_fill = '#334155' if is_dark else '#cbd5e1'
    grid_dot_opacity = '0.6' if is_dark else '0.5'
    bus_bar_ok = '#38bdf8' if is_dark else '#0f172a'
    bus_bar_bad = '#ef4444' if is_dark else '#dc2626'
    line_stroke = '#64748b' if is_dark else '#475569'
    bus_label_color = '#f8fafc' if is_dark else '#0f172a'
    ctrl_bg = 'rgba(30, 41, 59, 0.92)' if is_dark else 'rgba(255, 255, 255, 0.95)'
    ctrl_border = '#475569' if is_dark else '#cbd5e1'
    ctrl_text = '#e2e8f0' if is_dark else '#0f172a'
    card_bg = 'rgba(15, 23, 42, 0.96)' if is_dark else 'rgba(255, 255, 255, 0.98)'
    card_border = '#38bdf8' if is_dark else '#0284c7'
    card_text = '#e2e8f0' if is_dark else '#0f172a'
    card_label_col = '#94a3b8' if is_dark else '#64748b'
    card_row_border = '#334155' if is_dark else '#e2e8f0'
    flow_bubble_bg = '#1e293b' if is_dark else '#ffffff'
    flow_bubble_text = '#f8fafc' if is_dark else '#0f172a'
    flow_bubble_sub = '#94a3b8' if is_dark else '#64748b'
    gen_color = '#38bdf8' if is_dark else '#0284c7'
    load_color = '#fb923c' if is_dark else '#ea580c'

    # Language tokens
    is_vi = (lang == 'vi')
    search_placeholder = "🔍 Tìm Bus (VD: 1, 14, 50)..." if is_vi else "🔍 Search Bus (e.g. 1, 14, 50)..."
    guide_text = ("🖱️ Kéo để di chuyển | Cuộn chuột để Phóng to/Thu nhỏ | Bấm vào nút/nhánh để soi chi tiết"
                  if is_vi else "🖱️ Drag to pan | Mouse wheel to zoom | Click bus/line to inspect")
    center_btn_text = "🎯 Định vị vào trung tâm màn hình" if is_vi else "🎯 Center on Element"
    lbl_vm = "Điện áp nút Vm:" if is_vi else "Bus Voltage Vm:"
    lbl_va = "Góc lệch pha θ:" if is_vi else "Phase Angle θ:"
    lbl_pg = "Công suất phát Pg:" if is_vi else "Generation Pg:"
    lbl_qg = "Công suất phản kháng Qg:" if is_vi else "Reactive Gen Qg:"
    lbl_pd = "Công suất phụ tải Pd:" if is_vi else "Load Demand Pd:"
    lbl_qd = "Phụ tải phản kháng Qd:" if is_vi else "Reactive Load Qd:"
    lbl_conns = "Liên kết nhánh nối:" if is_vi else "Connected Branches:"
    lbl_pflow = "Dòng công suất P:" if is_vi else "Active Flow P:"
    lbl_qflow = "Dòng phản kháng Q:" if is_vi else "Reactive Flow Q:"
    lbl_ploss = "Tổn thất công suất:" if is_vi else "Active Losses:"
    lbl_r = "Điện trở R:" if is_vi else "Resistance R:"
    lbl_x = "Điện kháng X:" if is_vi else "Reactance X:"
    lbl_norm = "Bình thường" if is_vi else "Normal"
    lbl_viol = "Vi phạm" if is_vi else "Violation"

    bar_w = 64
    bar_h = 10

    # Index results for lookup
    b_map = {}
    if b_res is not None and not b_res.empty:
        for _, row in b_res.iterrows():
            b_map[int(row['bus'])] = row

    l_map = {}
    connected_branches_by_bus = {bid: [] for bid in bus_ids}

    if l_res is not None and not l_res.empty:
        for _, row in l_res.iterrows():
            fb, tb = int(row['from_bus']), int(row['to_bus'])
            l_map[(fb, tb)] = row
            if fb in connected_branches_by_bus:
                connected_branches_by_bus[fb].append({
                    'target': tb, 'p': float(row['p_from_MW']), 'q': float(row['q_from_Mvar']), 'loss': float(row['p_loss_MW'])
                })
            if tb in connected_branches_by_bus:
                connected_branches_by_bus[tb].append({
                    'target': fb, 'p': float(row['p_to_MW']), 'q': float(row['q_to_Mvar']), 'loss': float(row['p_loss_MW'])
                })

    svg = []
    # 1. DRAW TRANSMISSION LINES
    line_w = 2.8
    for idx, l_row in lines.iterrows():
        fb = int(l_row['from_bus'])
        tb = int(l_row['to_bus'])
        if fb not in coords or tb not in coords:
            continue
        x1, y1 = coords[fb]
        x2, y2 = coords[tb]
        r_val = float(l_row.get('r_pu', 0.0))
        x_val = float(l_row.get('x_pu', 0.0))

        res = l_map.get((fb, tb))
        if res is None:
            res = l_map.get((tb, fb))

        p_flow = 0.0
        q_flow = 0.0
        p_loss = 0.0
        if res is not None:
            is_forward = (res['from_bus'] == fb)
            p_flow = float(res['p_from_MW']) if is_forward else float(res['p_to_MW'])
            q_flow = float(res['q_from_Mvar']) if is_forward else float(res['q_to_Mvar'])
            p_loss = float(res['p_loss_MW'])

        line_attrs = (f'data-from="{fb}" data-to="{tb}" data-pflow="{p_flow:.2f}" '
                      f'data-qflow="{q_flow:.2f}" data-ploss="{p_loss:.2f}" '
                      f'data-r="{r_val:.5f}" data-x="{x_val:.5f}"')

        svg.append(f'<g class="line-group" {line_attrs} id="line-{fb}-{tb}">')
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="transparent" stroke-width="16" />')
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="trans-line" stroke="{line_stroke}" stroke-width="{line_w}" stroke-linecap="round" />')

        if res is not None:
            dx = x2 - x1
            dy = y2 - y1
            dist = math.hypot(dx, dy)
            if dist > 0:
                ux, uy = dx / dist, dy / dist
                nx, ny = -uy, ux

                if abs(p_flow) > 0.02:
                    ax1 = x1 + ux * (bar_w // 2 + 6)
                    ay1 = y1 + uy * (bar_w // 2 + 6)
                    ax2 = x2 - ux * (bar_w // 2 + 6)
                    ay2 = y2 - uy * (bar_w // 2 + 6)
                    if p_flow < 0:
                        ax1, ax2 = ax2, ax1
                        ay1, ay2 = ay2, ay1

                    svg.append(f'<line x1="{ax1}" y1="{ay1}" x2="{ax2}" y2="{ay2}" class="flow-animated" '
                               f'stroke="#10b981" stroke-width="2.2" stroke-dasharray="6,6" />')

                mx = x1 + dx * 0.5 + nx * 22
                my = y1 + dy * 0.5 + ny * 22
                flow_dir_arrow = '➜' if p_flow >= 0 else '⬅'
                svg.append(f'''
                <g class="flow-bubble" transform="translate({mx - 42}, {my - 14})">
                  <rect width="84" height="26" rx="4" fill="{flow_bubble_bg}" stroke="#0284c7" stroke-width="1" />
                  <text x="42" y="11" text-anchor="middle" font-size="9" font-weight="700" fill="{flow_bubble_text}">
                    {flow_dir_arrow} {abs(p_flow):.1f} MW
                  </text>
                  <text x="42" y="21" text-anchor="middle" font-size="7.5" fill="{flow_bubble_sub}">
                    Loss: {p_loss:.2f} MW
                  </text>
                </g>
                ''')

        svg.append('</g>')

    # 2. DRAW BUSES AND ATTACHED ELEMENTS
    for _, b_row in buses.iterrows():
        bid = int(b_row['bus'])
        if bid not in coords:
            continue
        bx, by = coords[bid]
        b_type = str(b_row.get('type', 'PQ'))

        res = b_map.get(bid)
        if res is not None:
            vm = float(res['vm_pu'])
            va = float(res['va_deg'])
            pg_mw = float(res['pg_MW'])
            qg_mvar = float(res['qg_Mvar'])
            pd_mw = float(res['pd_MW'])
            qd_mvar = float(res['qd_Mvar'])
        else:
            vm = float(b_row.get('vm_pu', 1.0))
            va = float(b_row.get('va_deg', 0.0))
            pg_mw = float(b_row.get('pg_pu', 0.0)) * base_mva
            qg_mvar = float(b_row.get('qg_pu', 0.0)) * base_mva
            pd_mw = float(b_row.get('pd_pu', 0.0)) * base_mva
            qd_mvar = float(b_row.get('qd_pu', 0.0)) * base_mva

        is_normal = (0.95 <= vm <= 1.05)
        bus_color = bus_bar_ok if is_normal else bus_bar_bad

        conns = connected_branches_by_bus.get(bid, [])
        conns_str = "; ".join([f"➜ Bus {c['target']}: {c['p']:.1f} MW" for c in conns[:4]])

        bus_attrs = (f'data-bus-id="{bid}" data-type="{b_type}" data-vm="{vm:.4f}" '
                     f'data-va="{va:.2f}" data-pg="{pg_mw:.2f}" data-qg="{qg_mvar:.2f}" '
                     f'data-pd="{pd_mw:.2f}" data-qd="{qd_mvar:.2f}" '
                     f'data-normal="{"1" if is_normal else "0"}" '
                     f'data-conns="{conns_str}"')

        svg.append(f'<g class="bus-group" id="bus-{bid}" {bus_attrs}>')
        svg.append(f'<circle cx="{bx}" cy="{by}" r="28" fill="transparent" />')

        # Bus bar
        svg.append(f'<rect x="{bx - bar_w/2}" y="{by - bar_h/2}" width="{bar_w}" height="{bar_h}" rx="3" '
                   f'class="pw-bus-bar" fill="{bus_color}" stroke="{ctrl_border}" stroke-width="1.2" />')

        # Bus label
        type_str = f" [{b_type}]"
        svg.append(f'<text x="{bx}" y="{by - bar_h/2 - 5}" text-anchor="middle" font-size="11" font-weight="700" fill="{bus_label_color}" class="bus-label">'
                   f'Bus {bid}{type_str}</text>')

        # Voltage badge (visible in LOD mid & near)
        v_bg = "rgba(16, 185, 129, 0.15)" if is_normal else "rgba(239, 68, 68, 0.2)"
        v_border = "#10b981" if is_normal else "#ef4444"
        v_text_color = "#10b981" if is_normal else "#ef4444"
        badge_w = 76
        badge_h = 20
        svg.append(f'''
        <g class="v-badge" transform="translate({bx - badge_w/2}, {by + bar_h/2 + 5})">
          <rect width="{badge_w}" height="{badge_h}" rx="4" fill="{v_bg}" stroke="{v_border}" stroke-width="1.2" />
          <text x="{badge_w/2}" y="{badge_h*0.7}" text-anchor="middle" font-size="10" font-weight="700" fill="{v_text_color}">
            {vm:.4f} pu
          </text>
        </g>
        ''')

        # Generator element
        has_gen = (b_type in ['Slack', 'PV']) or (pg_mw > 0.01)
        if has_gen:
            gx = bx - bar_w // 2 - 18
            gy = by - 12
            r_gen = 13
            svg.append(f'<path class="gen-arrow" d="M {gx} {gy+r_gen} L {gx} {by} L {bx - bar_w/2} {by}" fill="none" stroke="{gen_color}" stroke-width="2" />')
            svg.append(f'<circle class="gen-arrow" cx="{gx}" cy="{gy}" r="{r_gen}" fill="{flow_bubble_bg}" stroke="{gen_color}" stroke-width="2" />')
            svg.append(f'<path class="gen-arrow" d="M {gx-r_gen/2} {gy} Q {gx-r_gen/4} {gy-r_gen/3} {gx} {gy} T {gx+r_gen/2} {gy}" fill="none" stroke="{gen_color}" stroke-width="2" />')

            svg.append(f'''
            <g class="micro-callout" transform="translate({gx - 40}, {gy - 42})">
              <rect width="80" height="26" rx="4" fill="{flow_bubble_bg}" stroke="{gen_color}" stroke-width="1" />
              <text x="40" y="11" text-anchor="middle" font-size="8.5" font-weight="700" fill="{gen_color}">GEN {bid}</text>
              <text x="40" y="21" text-anchor="middle" font-size="8" fill="{flow_bubble_text}">{pg_mw:.1f} MW</text>
            </g>
            ''')

        # Load element
        if pd_mw > 0.01 or b_type == 'PQ':
            lx = bx + bar_w // 2 - 8
            ly = by + bar_h // 2
            svg.append(f'<line class="load-arrow" x1="{lx}" y1="{ly}" x2="{lx}" y2="{ly + 22}" stroke="{load_color}" stroke-width="2.2" marker-end="url(#arrLoad)" />')

            if pd_mw > 0.01:
                svg.append(f'''
                <g class="micro-callout" transform="translate({lx + 6}, {ly + 6})">
                  <rect width="76" height="24" rx="4" fill="{flow_bubble_bg}" stroke="{load_color}" stroke-width="1" />
                  <text x="38" y="10" text-anchor="middle" font-size="8.5" font-weight="700" fill="{load_color}">LOAD {bid}</text>
                  <text x="38" y="19" text-anchor="middle" font-size="8" fill="{flow_bubble_text}">{pd_mw:.1f} MW</text>
                </g>
                ''')

        svg.append('</g>')

    svg_body = "\n".join(svg)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body, html {{ width: 100%; height: 100%; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: {bg_style}; color: {card_text}; }}

  #pw-map-viewport {{
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: {bg_style};
    cursor: grab;
    user-select: none;
  }}
  #pw-map-viewport:active {{
    cursor: grabbing;
  }}

  /* Top Left Search & Status Bar */
  .map-search-bar {{
    position: absolute;
    top: 14px;
    left: 14px;
    z-index: 100;
    display: flex;
    gap: 8px;
    align-items: center;
  }}
  .map-search-input {{
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    color: {ctrl_text};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    width: 210px;
    outline: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    backdrop-filter: blur(6px);
    transition: all 0.2s;
  }}
  .map-search-input:focus {{
    border-color: #38bdf8;
    width: 250px;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3);
  }}
  .map-search-input::placeholder {{
    color: {card_label_col};
  }}
  .system-badge {{
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    color: #38bdf8;
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    backdrop-filter: blur(6px);
  }}

  /* Top Right Floating Navigation Tools */
  .map-ctrl-panel {{
    position: absolute;
    top: 14px;
    right: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 100;
    align-items: flex-end;
  }}
  .map-btn-group {{
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    backdrop-filter: blur(6px);
  }}
  .map-btn {{
    background: transparent;
    border: none;
    color: {ctrl_text};
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }}
  .map-btn:hover {{
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
  }}
  .map-btn:not(:last-child) {{
    border-bottom: 1px solid {ctrl_border};
  }}
  .zoom-indicator {{
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    color: #38bdf8;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    text-align: center;
    backdrop-filter: blur(4px);
    width: 100%;
  }}
  .lod-toggle {{
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    color: {card_label_col};
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 11px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    backdrop-filter: blur(4px);
    transition: all 0.15s;
  }}
  .lod-toggle:hover {{
    color: {ctrl_text};
    border-color: #38bdf8;
  }}

  /* Floating Inspector Card (InfoWindow) */
  #inspector-card {{
    position: absolute;
    bottom: 20px;
    left: 14px;
    width: 330px;
    background: {card_bg};
    border: 1.5px solid {card_border};
    border-radius: 12px;
    padding: 14px;
    color: {card_text};
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    z-index: 120;
    display: none;
    animation: slideUp 0.18s ease-out;
  }}
  @keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid {card_row_border};
    padding-bottom: 8px;
    margin-bottom: 10px;
  }}
  .card-title {{
    font-size: 14px;
    font-weight: 700;
    color: #0284c7;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .card-close {{
    background: transparent;
    border: none;
    color: {card_label_col};
    font-size: 18px;
    cursor: pointer;
    line-height: 1;
    padding: 2px 6px;
  }}
  .card-close:hover {{
    color: #ef4444;
  }}
  .card-row {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    margin-bottom: 6px;
  }}
  .card-label {{
    color: {card_label_col};
  }}
  .card-value {{
    color: {card_text};
    font-weight: 600;
    font-family: 'Consolas', monospace;
  }}
  .card-badge-ok {{
    color: #10b981;
    font-weight: 700;
  }}
  .card-badge-bad {{
    color: #ef4444;
    font-weight: 700;
  }}
  .card-btn {{
    background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%);
    border: none;
    color: white;
    padding: 7px 12px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    margin-top: 8px;
    transition: background 0.15s;
  }}
  .card-btn:hover {{
    background: #0284c7;
  }}

  /* Bottom Right Navigation & LOD Guide */
  .map-guide {{
    position: absolute;
    bottom: 14px;
    right: 14px;
    background: {ctrl_bg};
    border: 1px solid {ctrl_border};
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 11px;
    color: {card_label_col};
    z-index: 100;
    backdrop-filter: blur(4px);
    pointer-events: none;
  }}

  /* LOD Rules */
  .lod-far .micro-callout,
  .lod-far .flow-bubble,
  .lod-far .v-badge {{
    display: none !important;
  }}
  .lod-far .bus-label {{
    font-size: 13px !important;
    font-weight: 800 !important;
  }}
  .lod-far .pw-bus-bar {{
    stroke-width: 2.2px !important;
  }}

  .lod-mid .micro-callout {{
    display: none !important;
  }}

  /* Selection Highlight */
  .node-active rect.pw-bus-bar {{
    stroke: #f59e0b !important;
    stroke-width: 4px !important;
    filter: drop-shadow(0 0 10px #f59e0b);
  }}
  .line-active line.trans-line {{
    stroke: #f59e0b !important;
    stroke-width: 4.5px !important;
    filter: drop-shadow(0 0 8px #f59e0b);
  }}

  /* Hover States */
  .bus-group {{
    cursor: pointer;
  }}
  .bus-group:hover rect.pw-bus-bar {{
    stroke: #38bdf8;
    stroke-width: 3px;
    filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.6));
  }}
  .line-group {{
    cursor: pointer;
  }}
  .line-group:hover line.trans-line {{
    stroke: #38bdf8;
    stroke-width: 3.5px;
  }}

  @keyframes flowDash {{
    from {{ stroke-dashoffset: 28; }}
    to {{ stroke-dashoffset: 0; }}
  }}
  .flow-animated {{
    animation: flowDash 1.2s linear infinite;
  }}
</style>
</head>
<body>

<div id="pw-map-viewport">
  <div class="map-search-bar">
    <input type="text" id="bus-search" class="map-search-input" placeholder="{search_placeholder}" />
    <div class="system-badge">⚡ {n_buses} BUSES | {len(lines)} LINES</div>
  </div>

  <div class="map-ctrl-panel">
    <div class="map-btn-group">
      <button class="map-btn" id="btn-zoom-in" title="Phóng to (+)">+</button>
      <button class="map-btn" id="btn-zoom-out" title="Thu nhỏ (-)">−</button>
      <button class="map-btn" id="btn-fit" title="Căn vừa màn hình (Fit to Screen)">⛶</button>
    </div>
    <div class="zoom-indicator" id="zoom-badge">100%</div>
    <button class="lod-toggle" id="btn-toggle-lod" title="Toggle Detail Level">
      👁️ <span id="lod-text">Auto LOD</span>
    </button>
  </div>

  <div id="inspector-card">
    <div class="card-header">
      <div class="card-title" id="card-title">⚡ Bus Inspector</div>
      <button class="card-close" id="btn-close-card">✕</button>
    </div>
    <div id="card-content"></div>
    <button class="card-btn" id="btn-card-center">{center_btn_text}</button>
  </div>

  <div class="map-guide">{guide_text}</div>

  <svg id="main-svg" width="100%" height="100%" viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="pwGrid" width="30" height="30" patternUnits="userSpaceOnUse">
        <circle cx="3" cy="3" r="1.2" fill="{grid_dot_fill}" opacity="{grid_dot_opacity}" />
      </pattern>
      <marker id="arrLoad" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 0 L 10 0 L 5 8 z" fill="{load_color}" />
      </marker>
    </defs>

    <rect width="100%" height="100%" fill="url(#pwGrid)" pointer-events="none" />

    <g id="viewport-group" class="lod-mid" transform="matrix(1 0 0 1 0 0)">
      {svg_body}
    </g>
  </svg>
</div>

<script>
(function() {{
  const viewport = document.getElementById('pw-map-viewport');
  const g = document.getElementById('viewport-group');
  const zoomBadge = document.getElementById('zoom-badge');
  const inspectorCard = document.getElementById('inspector-card');
  const cardTitle = document.getElementById('card-title');
  const cardContent = document.getElementById('card-content');
  const btnCloseCard = document.getElementById('btn-close-card');
  const btnCardCenter = document.getElementById('btn-card-center');
  const searchInput = document.getElementById('bus-search');
  const btnToggleLod = document.getElementById('btn-toggle-lod');
  const lodText = document.getElementById('lod-text');

  const canvasWidth = {canvas_w};
  const canvasHeight = {canvas_h};

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;
  let isDragging = false;
  let startX = 0;
  let startY = 0;
  let forceFullDetail = false;
  let currentTargetCoord = null;

  function fitView() {{
    const rect = viewport.getBoundingClientRect();
    const pad = 40;
    const sX = (rect.width - pad) / canvasWidth;
    const sY = (rect.height - pad) / canvasHeight;
    scale = Math.min(sX, sY, 1.25);
    translateX = (rect.width - canvasWidth * scale) / 2;
    translateY = (rect.height - canvasHeight * scale) / 2;
    applyTransform();
  }}

  function applyTransform() {{
    g.setAttribute('transform', `matrix(${{scale}} 0 0 ${{scale}} ${{translateX}} ${{translateY}})`);
    zoomBadge.textContent = `${{Math.round(scale * 100)}}%`;
    updateLOD();
  }}

  function updateLOD() {{
    if (forceFullDetail) {{
      g.className.baseVal = 'lod-near';
      return;
    }}
    if (scale < 0.70) {{
      g.className.baseVal = 'lod-far';
    }} else if (scale < 1.30) {{
      g.className.baseVal = 'lod-mid';
    }} else {{
      g.className.baseVal = 'lod-near';
    }}
  }}

  viewport.addEventListener('mousedown', (e) => {{
    if (e.target.closest('#inspector-card') || e.target.closest('.map-ctrl-panel') || e.target.closest('.map-search-bar')) return;
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
  }});

  window.addEventListener('mousemove', (e) => {{
    if (!isDragging) return;
    translateX += (e.clientX - startX);
    translateY += (e.clientY - startY);
    startX = e.clientX;
    startY = e.clientY;
    applyTransform();
  }});

  window.addEventListener('mouseup', () => {{
    isDragging = false;
  }});

  viewport.addEventListener('wheel', (e) => {{
    e.preventDefault();
    const rect = viewport.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    const canvasX = (mx - translateX) / scale;
    const canvasY = (my - translateY) / scale;

    const factor = e.deltaY < 0 ? 1.18 : 0.85;
    const newScale = Math.min(Math.max(scale * factor, 0.15), 5.0);

    translateX = mx - canvasX * newScale;
    translateY = my - canvasY * newScale;
    scale = newScale;
    applyTransform();
  }}, {{ passive: false }});

  document.getElementById('btn-zoom-in').addEventListener('click', () => {{
    const rect = viewport.getBoundingClientRect();
    const mx = rect.width / 2;
    const my = rect.height / 2;
    const canvasX = (mx - translateX) / scale;
    const canvasY = (my - translateY) / scale;
    scale = Math.min(scale * 1.25, 5.0);
    translateX = mx - canvasX * scale;
    translateY = my - canvasY * scale;
    applyTransform();
  }});

  document.getElementById('btn-zoom-out').addEventListener('click', () => {{
    const rect = viewport.getBoundingClientRect();
    const mx = rect.width / 2;
    const my = rect.height / 2;
    const canvasX = (mx - translateX) / scale;
    const canvasY = (my - translateY) / scale;
    scale = Math.max(scale * 0.8, 0.15);
    translateX = mx - canvasX * scale;
    translateY = my - canvasY * scale;
    applyTransform();
  }});

  document.getElementById('btn-fit').addEventListener('click', fitView);

  btnToggleLod.addEventListener('click', () => {{
    forceFullDetail = !forceFullDetail;
    lodText.textContent = forceFullDetail ? 'Full Detail (Locked)' : 'Auto LOD';
    updateLOD();
  }});

  function clearHighlights() {{
    document.querySelectorAll('.node-active').forEach(el => el.classList.remove('node-active'));
    document.querySelectorAll('.line-active').forEach(el => el.classList.remove('line-active'));
  }}

  document.querySelectorAll('.bus-group').forEach(busEl => {{
    busEl.addEventListener('click', (e) => {{
      e.stopPropagation();
      clearHighlights();
      busEl.classList.add('node-active');

      const bid = busEl.getAttribute('data-bus-id');
      const btype = busEl.getAttribute('data-type');
      const vm = busEl.getAttribute('data-vm');
      const va = busEl.getAttribute('data-va');
      const pg = busEl.getAttribute('data-pg');
      const qg = busEl.getAttribute('data-qg');
      const pd = busEl.getAttribute('data-pd');
      const qd = busEl.getAttribute('data-qd');
      const isNorm = busEl.getAttribute('data-normal') === '1';
      const conns = busEl.getAttribute('data-conns');

      cardTitle.innerHTML = `⚡ Bus ${{bid}} <span style="font-size:11px;color:#94a3b8;">[${{btype}}]</span>`;
      currentTargetCoord = {{ id: bid, el: busEl }};

      cardContent.innerHTML = `
        <div class="card-row">
          <span class="card-label">{lbl_vm}</span>
          <span class="card-value ${{isNorm ? 'card-badge-ok' : 'card-badge-bad'}}">${{vm}} pu (${{isNorm ? '{lbl_norm}' : '{lbl_viol}'}})</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_va}</span>
          <span class="card-value">${{va}}°</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_pg}</span>
          <span class="card-value" style="color:#0284c7;">${{pg}} MW</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_qg}</span>
          <span class="card-value">${{qg}} MVAR</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_pd}</span>
          <span class="card-value" style="color:#ea580c;">${{pd}} MW</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_qd}</span>
          <span class="card-value">${{qd}} MVAR</span>
        </div>
        ${{conns ? `
        <div style="margin-top:8px;padding-top:8px;border-top:1px solid {card_row_border};">
          <div style="font-size:11px;color:{card_label_col};margin-bottom:4px;font-weight:600;">{lbl_conns}</div>
          <div style="font-size:11px;line-height:1.4;">${{conns}}</div>
        </div>
        ` : ''}}
      `;

      inspectorCard.style.display = 'block';
    }});
  }});

  document.querySelectorAll('.line-group').forEach(lineEl => {{
    lineEl.addEventListener('click', (e) => {{
      e.stopPropagation();
      clearHighlights();
      lineEl.classList.add('line-active');

      const fb = lineEl.getAttribute('data-from');
      const tb = lineEl.getAttribute('data-to');
      const pflow = lineEl.getAttribute('data-pflow');
      const qflow = lineEl.getAttribute('data-qflow');
      const ploss = lineEl.getAttribute('data-ploss');
      const r = lineEl.getAttribute('data-r');
      const x = lineEl.getAttribute('data-x');

      cardTitle.innerHTML = `🔗 Line ${{fb}} ➜ ${{tb}}`;
      currentTargetCoord = null;

      cardContent.innerHTML = `
        <div class="card-row">
          <span class="card-label">{lbl_pflow}</span>
          <span class="card-value" style="color:#10b981;">${{pflow}} MW</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_qflow}</span>
          <span class="card-value">${{qflow}} MVAR</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_ploss}</span>
          <span class="card-value" style="color:#ef4444;">${{ploss}} MW</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_r}</span>
          <span class="card-value">${{r}} pu</span>
        </div>
        <div class="card-row">
          <span class="card-label">{lbl_x}</span>
          <span class="card-value">${{x}} pu</span>
        </div>
      `;

      inspectorCard.style.display = 'block';
    }});
  }});

  btnCloseCard.addEventListener('click', () => {{
    inspectorCard.style.display = 'none';
    clearHighlights();
  }});

  btnCardCenter.addEventListener('click', () => {{
    if (!currentTargetCoord) return;
    centerOnBus(currentTargetCoord.id);
  }});

  function centerOnBus(busId) {{
    const el = document.getElementById(`bus-${{busId}}`);
    if (!el) return;
    clearHighlights();
    el.classList.add('node-active');

    const rect = el.querySelector('rect');
    if (!rect) return;
    const bx = parseFloat(rect.getAttribute('x')) + parseFloat(rect.getAttribute('width')) / 2;
    const by = parseFloat(rect.getAttribute('y')) + parseFloat(rect.getAttribute('height')) / 2;

    const vRect = viewport.getBoundingClientRect();
    scale = Math.max(scale, 1.4);
    translateX = vRect.width / 2 - bx * scale;
    translateY = vRect.height / 2 - by * scale;
    applyTransform();
    el.dispatchEvent(new MouseEvent('click', {{ bubbles: false }}));
  }}

  searchInput.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') {{
      const query = searchInput.value.trim().replace(/^bus\\s*/i, '');
      if (query) {{
        centerOnBus(query);
      }}
    }}
  }});

  window.addEventListener('load', fitView);
  window.addEventListener('resize', fitView);
  setTimeout(fitView, 50);

}})();
</script>
</body>
</html>
"""
    return html
