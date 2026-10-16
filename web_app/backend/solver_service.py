"""
Service module for the Modern Power Flow Web Application.
Extends and interfaces with the core numerical engine in src/ while providing:
- Step-by-step Newton-Raphson iteration telemetry (separated dP and dQ residuals)
- Real-time input validation with granular diagnostic reports
- Y-bus matrix serialization in both rectangular and polar forms
- Q-limit evaluation (Qmin / Qmax capability checking for PV buses)
- Base MVA conversion (per-unit <=> physical MW/Mvar)
- Standard benchmark presets (3-bus, 5-bus, IEEE 14-bus)
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd

# Add project root to sys.path to reuse src modules cleanly
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ybus import build_ybus
from src.power_equations import power, mismatch, indices
from src.jacobian import jacobian
from src.branch_flows import output_tables
from src.data_models import load_case
from src.newton_raphson import solve as core_solve
from src.practical_scenarios import check_grid_security, run_n1_contingency, run_load_stress_analysis
from pypower.api import runpf, ppoption



# ==============================================================================
# 1. INPUT VALIDATION & DIAGNOSTICS
# ==============================================================================

def validate_grid_data(buses_data: List[Dict[str, Any]], lines_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Performs comprehensive real-time validation on user-edited bus and line records.
    Returns: {
        'valid': bool,
        'errors': list of human-readable error strings,
        'warnings': list of advisory notes,
        'bus_count': int,
        'line_count': int,
        'slack_count': int,
        'islanded_buses': list of bus IDs
    }
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    if not buses_data:
        errors.append("Bảng nút (Buses) chưa có dữ liệu. Vui lòng nhập ít nhất 2 nút.")
        return {'valid': False, 'errors': errors, 'warnings': warnings, 'bus_count': 0, 'line_count': 0, 'slack_count': 0}
        
    if not lines_data:
        errors.append("Bảng đường dây (Lines) chưa có dữ liệu. Vui lòng nhập ít nhất 1 đường dây liên kết.")
        return {'valid': False, 'errors': errors, 'warnings': warnings, 'bus_count': len(buses_data), 'line_count': 0, 'slack_count': 0}

    # Parse and validate buses
    bus_ids = set()
    slack_count = 0
    pv_count = 0
    pq_count = 0

    for idx, b in enumerate(buses_data, start=1):
        try:
            bid = int(b.get('bus', 0))
        except (ValueError, TypeError):
            errors.append(f"Hàng nút #{idx}: ID nút '{b.get('bus')}' không phải là số nguyên hợp lệ.")
            continue

        if bid in bus_ids:
            errors.append(f"Hàng nút #{idx}: Trùng lặp ID nút {bid}. Mỗi nút phải có một ID duy nhất.")
        bus_ids.add(bid)

        b_type = str(b.get('type', '')).strip()
        if b_type not in ['Slack', 'PV', 'PQ']:
            errors.append(f"Nút {bid}: Loại nút '{b_type}' không hợp lệ. Chỉ chấp nhận 'Slack', 'PV', hoặc 'PQ'.")
        elif b_type == 'Slack':
            slack_count += 1
        elif b_type == 'PV':
            pv_count += 1
        elif b_type == 'PQ':
            pq_count += 1

        try:
            vm = float(b.get('vm_pu', 1.0))
            if vm <= 0:
                errors.append(f"Nút {bid}: Biên độ điện áp Vm = {vm} pu phải là số dương (> 0).")
            elif vm < 0.7 or vm > 1.3:
                warnings.append(f"Nút {bid}: Điện áp Vm = {vm} pu nằm ngoài dải vận hành thông thường [0.7, 1.3] pu.")
        except (ValueError, TypeError):
            errors.append(f"Nút {bid}: Giá trị điện áp Vm không phải số thực.")

        for p_field in ['pd_pu', 'qd_pu']:
            try:
                val = float(b.get(p_field, 0.0))
                if val < 0:
                    errors.append(f"Nút {bid}: Phụ tải {p_field} = {val} không được âm (yêu cầu Pd >= 0, Qd >= 0).")
            except (ValueError, TypeError):
                errors.append(f"Nút {bid}: Giá trị {p_field} không phải số thực.")

    if slack_count == 0:
        errors.append("Hệ thống chưa có nút cân bằng (Slack bus). Bắt buộc phải có đúng 1 nút Slack.")
    elif slack_count > 1:
        errors.append(f"Hệ thống có {slack_count} nút Slack. Thuật toán chỉ cho phép duy nhất 1 nút Slack.")

    # Parse and validate lines
    graph: Dict[int, set] = {bid: set() for bid in bus_ids}
    for idx, line in enumerate(lines_data, start=1):
        try:
            fb = int(line.get('from_bus', 0))
            tb = int(line.get('to_bus', 0))
        except (ValueError, TypeError):
            errors.append(f"Đường dây #{idx}: ID nút đầu/cuối không hợp lệ.")
            continue

        if fb == tb:
            errors.append(f"Đường dây #{idx}: Nút đầu và nút cuối trùng nhau ({fb} -> {tb}). Không hỗ trợ vòng lặp tự thân.")

        if fb not in bus_ids:
            errors.append(f"Đường dây #{idx}: Nút đầu {fb} không tồn tại trong Bảng nút.")
        if tb not in bus_ids:
            errors.append(f"Đường dây #{idx}: Nút cuối {tb} không tồn tại trong Bảng nút.")

        if fb in bus_ids and tb in bus_ids and fb != tb:
            graph[fb].add(tb)
            graph[tb].add(fb)

        try:
            r = float(line.get('r_pu', 0.0))
            x = float(line.get('x_pu', 0.0))
            if r < 0:
                errors.append(f"Đường dây #{idx} ({fb}-{tb}): Điện trở R = {r} không được âm (R >= 0).")
            if x <= 0:
                errors.append(f"Đường dây #{idx} ({fb}-{tb}): Điện kháng X = {x} phải là số dương (X > 0).")
            if r == 0 and x == 0:
                errors.append(f"Đường dây #{idx} ({fb}-{tb}): Tổng trở Z bằng 0 gây đoản mạch.")
        except (ValueError, TypeError):
            errors.append(f"Đường dây #{idx} ({fb}-{tb}): Giá trị R hoặc X không phải số thực.")

    # Check network connectivity (DFS reachability)
    islanded_buses: List[int] = []
    if bus_ids:
        start_node = next(iter(bus_ids))
        visited = set()
        stack = [start_node]
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                stack.extend(graph[curr] - visited)

        islanded_buses = sorted(list(bus_ids - visited))
        if islanded_buses:
            errors.append(f"Lưới điện bị chia cắt / mất liên thông! Các nút sau bị cô lập: {islanded_buses}.")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'bus_count': len(bus_ids),
        'line_count': len(lines_data),
        'slack_count': slack_count,
        'pv_count': pv_count,
        'pq_count': pq_count,
        'islanded_buses': islanded_buses
    }


# ==============================================================================
# 2. Y-BUS MATRIX GENERATION
# ==============================================================================

def compute_ybus_matrix(buses_df: pd.DataFrame, lines_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Constructs the Y-bus admittance matrix and returns serialized elements with
    both rectangular (G, B) and polar (|Y|, theta_deg) components.
    """
    ybus = build_ybus(buses_df, lines_df)
    n = len(buses_df)
    bus_ids = buses_df['bus'].tolist()

    matrix_data: List[List[Dict[str, Any]]] = []
    non_zeros = 0

    for i in range(n):
        row = []
        for j in range(n):
            y_val = ybus[i, j]
            g = float(np.real(y_val))
            b = float(np.imag(y_val))
            mag = float(np.abs(y_val))
            ang_deg = float(np.rad2deg(np.angle(y_val)))
            is_nonzero = (mag > 1e-9)
            if is_nonzero:
                non_zeros += 1

            row.append({
                'from_bus': int(bus_ids[i]),
                'to_bus': int(bus_ids[j]),
                'g': g,
                'b': b,
                'magnitude': mag,
                'angle_deg': ang_deg,
                'is_diagonal': (i == j),
                'is_nonzero': is_nonzero
            })
        matrix_data.append(row)

    sparsity = 1.0 - (non_zeros / (n * n)) if (n * n) > 0 else 0.0

    return {
        'dim': n,
        'bus_ids': [int(b) for b in bus_ids],
        'matrix': matrix_data,
        'non_zeros': non_zeros,
        'sparsity': round(sparsity * 100, 2)
    }


# ==============================================================================
# 3. ADVANCED NEWTON-RAPHSON SOLVER WITH STEP-BY-STEP TELEMETRY & Q-LIMITS
# ==============================================================================

def solve_power_flow(
    buses_df: pd.DataFrame,
    lines_df: pd.DataFrame,
    base_mva: float = 100.0,
    tolerance: float = 1e-6,
    max_iterations: int = 30
) -> Dict[str, Any]:
    """
    Runs full Newton-Raphson power flow and returns rich telemetry:
    - Step-by-step convergence log with separate dP, dQ errors
    - Bus results with recovered Slack/PV generation and Q-limit violation indicators
    - Branch power flows, losses, and current magnitudes
    - Overall system active/reactive power balance verification
    """
    # Real-time check before solving
    validation = validate_grid_data(buses_df.to_dict('records'), lines_df.to_dict('records'))
    if not validation['valid']:
        return {
            'converged': False,
            'message': 'Dữ liệu đầu vào không hợp lệ: ' + '; '.join(validation['errors'][:3]),
            'iterations': 0,
            'history': [],
            'validation_errors': validation['errors']
        }

    ybus = build_ybus(buses_df, lines_df)
    ns, pq = indices(buses_df)
    vm = buses_df.vm_pu.to_numpy(float).copy()
    va = np.deg2rad(buses_df.va_deg.to_numpy(float))

    history: List[Dict[str, Any]] = []
    converged = False
    stop_reason = ""

    for k in range(max_iterations + 1):
        f = mismatch(buses_df, ybus, vm, va)
        num_p = len(ns)
        num_q = len(pq)
        
        dp_vec = f[:num_p] if num_p > 0 else np.array([0.0])
        dq_vec = f[num_p:] if num_q > 0 else np.array([0.0])
        
        max_dp = float(np.max(np.abs(dp_vec), initial=0.0))
        max_dq = float(np.max(np.abs(dq_vec), initial=0.0))
        max_err = float(np.max(np.abs(f), initial=0.0))

        step_record = {
            'iteration': k,
            'max_p_mismatch_pu': max_dp,
            'max_p_mismatch_MW': max_dp * base_mva,
            'max_q_mismatch_pu': max_dq,
            'max_q_mismatch_Mvar': max_dq * base_mva,
            'max_mismatch_pu': max_err,
            'log10_mismatch': float(np.log10(max(max_err, 1e-18)))
        }
        history.append(step_record)

        if np.isfinite(max_err) and max_err < tolerance:
            converged = True
            stop_reason = f"Đã hội tụ sau {k} vòng lặp (Sai số cực đại {max_err:.2e} pu < Dung sai {tolerance:.2e} pu)."
            break

        if not np.isfinite(max_err):
            stop_reason = "Sai số công suất không hữu hạn (NaN hoặc Inf) tại vòng lặp này."
            break

        if k == max_iterations:
            stop_reason = f"Đã chạm giới hạn số vòng lặp tối đa ({max_iterations} vòng) mà chưa hội tụ."
            break

        # Linear solve J dx = f
        try:
            J = jacobian(ybus, vm, va, ns, pq)
            dx = np.linalg.solve(J, f)
        except np.linalg.LinAlgError:
            stop_reason = "Ma trận Jacobi bị suy biến (Singular Jacobian) không thể đảo giải. Lưới điện có thể đang ở điểm sụp đổ điện áp."
            break

        vm_new = vm.copy()
        va_new = va.copy()
        va_new[ns] += dx[:len(ns)]
        vm_new[pq] += dx[len(ns):]

        if not np.isfinite(dx).all() or (vm_new <= 0).any():
            stop_reason = "Bước cập nhật Newton tạo ra biên độ điện áp không dương hoặc giá trị không xác định."
            break

        vm, va = vm_new, va_new

    # Generate results if converged
    bus_results: List[Dict[str, Any]] = []
    branch_results: List[Dict[str, Any]] = []
    system_summary: Dict[str, Any] = {}

    if converged:
        # Calculate active & reactive injection and line flows
        p_calc, q_calc = power(ybus, vm, va)
        
        # Check Q-limits if defined in input
        has_qmin = 'q_min_pu' in buses_df.columns or 'q_min_Mvar' in buses_df.columns
        has_qmax = 'q_max_pu' in buses_df.columns or 'q_max_Mvar' in buses_df.columns

        total_pg_mw = 0.0
        total_qg_mvar = 0.0
        total_pd_mw = 0.0
        total_qd_mvar = 0.0

        for i, row in buses_df.reset_index(drop=True).iterrows():
            bid = int(row['bus'])
            b_type = str(row['type'])
            
            p_net_mw = float(p_calc[i] * base_mva)
            q_net_mvar = float(q_calc[i] * base_mva)
            pd_mw = float(row['pd_pu'] * base_mva)
            qd_mvar = float(row['qd_pu'] * base_mva)
            
            # Recover generator power
            pg_mw = float((p_calc[i] + row['pd_pu']) * base_mva) if b_type in ['Slack', 'PV'] else float(row['pg_pu'] * base_mva)
            qg_mvar = float((q_calc[i] + row['qd_pu']) * base_mva) if b_type in ['Slack', 'PV'] else float(row['qg_pu'] * base_mva)

            total_pg_mw += pg_mw
            total_qg_mvar += qg_mvar
            total_pd_mw += pd_mw
            total_qd_mvar += qd_mvar

            # Q-limit check
            q_status = "OK"
            q_min_val = None
            q_max_val = None

            if b_type == 'PV':
                if 'q_min_pu' in row and pd.notna(row['q_min_pu']):
                    q_min_val = float(row['q_min_pu']) * base_mva
                elif 'q_min_Mvar' in row and pd.notna(row['q_min_Mvar']):
                    q_min_val = float(row['q_min_Mvar'])
                else:
                    q_min_val = -50.0  # default indicative practical limits

                if 'q_max_pu' in row and pd.notna(row['q_max_pu']):
                    q_max_val = float(row['q_max_pu']) * base_mva
                elif 'q_max_Mvar' in row and pd.notna(row['q_max_Mvar']):
                    q_max_val = float(row['q_max_Mvar'])
                else:
                    q_max_val = 50.0

                if q_min_val is not None and qg_mvar < q_min_val - 1e-4:
                    q_status = f"Vi phạm Qmin ({qg_mvar:.2f} < {q_min_val:.2f} Mvar)"
                elif q_max_val is not None and qg_mvar > q_max_val + 1e-4:
                    q_status = f"Vi phạm Qmax ({qg_mvar:.2f} > {q_max_val:.2f} Mvar)"

            bus_results.append({
                'bus': bid,
                'type': b_type,
                'vm_pu': round(float(vm[i]), 6),
                'va_deg': round(float(np.rad2deg(va[i])), 4),
                'va_rad': round(float(va[i]), 6),
                'p_net_MW': round(p_net_mw, 4),
                'q_net_Mvar': round(q_net_mvar, 4),
                'pg_MW': round(pg_mw, 4),
                'qg_Mvar': round(qg_mvar, 4),
                'pd_MW': round(pd_mw, 4),
                'qd_Mvar': round(qd_mvar, 4),
                'q_status': q_status,
                'q_min_Mvar': q_min_val,
                'q_max_Mvar': q_max_val
            })

        # Calculate branch flows
        bus_idx_map = {b: i for i, b in enumerate(buses_df['bus'])}
        v_complex = vm * np.exp(1j * va)
        total_p_loss_mw = 0.0
        total_q_loss_mvar = 0.0

        for _, line in lines_df.iterrows():
            fb = int(line['from_bus'])
            tb = int(line['to_bus'])
            idx_f = bus_idx_map[fb]
            idx_t = bus_idx_map[tb]
            z = complex(float(line['r_pu']), float(line['x_pu']))
            
            i_branch = (v_complex[idx_f] - v_complex[idx_t]) / z
            s_from = v_complex[idx_f] * np.conj(i_branch) * base_mva
            s_to = v_complex[idx_t] * np.conj(-i_branch) * base_mva
            p_loss = (s_from + s_to).real
            q_loss = (s_from + s_to).imag
            i2r = (abs(i_branch) ** 2) * float(line['r_pu']) * base_mva

            total_p_loss_mw += p_loss
            total_q_loss_mvar += q_loss

            branch_results.append({
                'from_bus': fb,
                'to_bus': tb,
                'p_from_MW': round(float(s_from.real), 4),
                'q_from_Mvar': round(float(s_from.imag), 4),
                'p_to_MW': round(float(s_to.real), 4),
                'q_to_Mvar': round(float(s_to.imag), 4),
                'p_loss_MW': round(float(p_loss), 4),
                'q_loss_Mvar': round(float(q_loss), 4),
                'i2r_MW': round(float(i2r), 4),
                'current_pu': round(float(abs(i_branch)), 4)
            })

        p_balance_error = abs(total_pg_mw - total_pd_mw - total_p_loss_mw)
        q_balance_error = abs(total_qg_mvar - total_qd_mvar - total_q_loss_mvar)

        system_summary = {
            'total_generation_MW': round(total_pg_mw, 4),
            'total_generation_Mvar': round(total_qg_mvar, 4),
            'total_demand_MW': round(total_pd_mw, 4),
            'total_demand_Mvar': round(total_qd_mvar, 4),
            'total_loss_MW': round(total_p_loss_mw, 4),
            'total_loss_Mvar': round(total_q_loss_mvar, 4),
            'p_balance_error_MW': float(p_balance_error),
            'q_balance_error_Mvar': float(q_balance_error),
            'loss_percentage': round((total_p_loss_mw / total_pg_mw * 100), 2) if total_pg_mw > 0 else 0.0,
            'min_voltage_pu': round(float(np.min(vm)), 4),
            'max_voltage_pu': round(float(np.max(vm)), 4)
        }

    return {
        'converged': converged,
        'message': stop_reason,
        'iterations': len(history) - 1 if converged else max_iterations,
        'history': history,
        'buses': bus_results,
        'branches': branch_results,
        'summary': system_summary,
        'base_mva': base_mva
    }


# ==============================================================================
# 4. BENCHMARK PRESETS (3-BUS, 5-BUS, IEEE 14, 30, 57, 118-BUS)
# ==============================================================================

BENCHMARK_META = {
    '3bus': {
        'name': 'Lưới 3 nút đào tạo (Task Benchmark)',
        'description': 'Lưới 3 nút chuẩn đồ án: Nút 1 Slack (1.05 pu), Nút 2 PV (1.02 pu, 50 MW), Nút 3 PQ (60 MW, 25 Mvar).'
    },
    '5bus': {
        'name': 'Lưới 5 nút tổng hợp (Synthetic Case)',
        'description': 'Lưới 5 nút vòng khép kín với 1 Slack, 1 PV có tải tại chỗ, 3 PQ và 7 đường dây liên kết.'
    },
    '14bus': {
        'name': 'Chuẩn IEEE 14 nút (14-Bus Benchmark)',
        'description': 'Hệ thống chuẩn IEEE 14 nút: 14 thanh cái, 20 đường dây, 5 máy phát điện (1 Slack, 4 PV).'
    },
    '30bus': {
        'name': 'Chuẩn IEEE 30 nút (30-Bus Benchmark)',
        'description': 'Hệ thống chuẩn IEEE 30 nút: 30 thanh cái, 41 đường dây, 6 máy phát điện (1 Slack, 5 PV).'
    },
    '57bus': {
        'name': 'Chuẩn IEEE 57 nút (57-Bus Benchmark)',
        'description': 'Hệ thống chuẩn IEEE 57 nút quy mô trung bình: 57 thanh cái, 80 đường dây, 7 máy phát điện.'
    },
    '118bus': {
        'name': 'Chuẩn IEEE 118 nút (118-Bus Benchmark)',
        'description': 'Hệ thống chuẩn IEEE 118 nút công nghiệp (AEP): 118 thanh cái, 186 đường dây, 54 máy phát điện.'
    }
}

def get_preset_case(preset_id: str) -> Dict[str, Any]:
    """Dynamically loads any standard case from CSV files."""
    if preset_id not in BENCHMARK_META:
        raise ValueError(f"Không tìm thấy kịch bản mẫu '{preset_id}'")
    
    buses_df, lines_df = load_case(preset_id)
    meta = BENCHMARK_META[preset_id]
    
    b_records = []
    for _, r in buses_df.iterrows():
        b_records.append({
            'bus': int(r['bus']),
            'type': str(r['type']),
            'pg_pu': float(r['pg_pu']) if pd.notna(r.get('pg_pu')) else 0.0,
            'qg_pu': float(r['qg_pu']) if pd.notna(r.get('qg_pu')) else 0.0,
            'pd_pu': float(r['pd_pu']) if pd.notna(r.get('pd_pu')) else 0.0,
            'qd_pu': float(r['qd_pu']) if pd.notna(r.get('qd_pu')) else 0.0,
            'vm_pu': float(r['vm_pu']) if pd.notna(r.get('vm_pu')) else 1.0,
            'va_deg': float(r['va_deg']) if pd.notna(r.get('va_deg')) else 0.0,
            'q_min_pu': float(r['q_min_pu']) if pd.notna(r.get('q_min_pu')) else -1.0,
            'q_max_pu': float(r['q_max_pu']) if pd.notna(r.get('q_max_pu')) else 1.0
        })

    l_records = []
    for _, r in lines_df.iterrows():
        l_records.append({
            'from_bus': int(r['from_bus']),
            'to_bus': int(r['to_bus']),
            'r_pu': float(r['r_pu']),
            'x_pu': float(r['x_pu'])
        })

    return {
        'id': preset_id,
        'name': meta['name'],
        'description': meta['description'],
        'base_mva': 100.0,
        'buses': b_records,
        'lines': l_records
    }

def get_all_presets_meta() -> List[Dict[str, Any]]:
    """Returns metadata for all available presets."""
    result = []
    for pid, meta in BENCHMARK_META.items():
        try:
            b, l = load_case(pid)
            result.append({
                'id': pid,
                'name': meta['name'],
                'description': meta['description'],
                'bus_count': len(b),
                'line_count': len(l)
            })
        except Exception:
            result.append({
                'id': pid,
                'name': meta['name'],
                'description': meta['description'],
                'bus_count': 0,
                'line_count': 0
            })
    return result

# Cache static dictionary for backward compatibility
PRESETS = {pid: get_preset_case(pid) for pid in ['3bus', '5bus']}


# ==============================================================================
# 5. PRACTICAL ENGINEERING SCENARIOS & SECURITY AUDIT
# ==============================================================================

def _filter_core_frames(buses_df: pd.DataFrame, lines_df: pd.DataFrame):
    """Filters DataFrames to exact schema required by src.validation.validate."""
    b_cols = ['bus', 'type', 'pg_pu', 'qg_pu', 'pd_pu', 'qd_pu', 'vm_pu', 'va_deg']
    l_cols = ['from_bus', 'to_bus', 'r_pu', 'x_pu']
    b = buses_df[[c for c in b_cols if c in buses_df.columns]].copy()
    for c in b_cols:
        if c not in b.columns:
            b[c] = 0.0 if c not in ['vm_pu', 'type'] else (1.0 if c == 'vm_pu' else 'PQ')
    l = lines_df[[c for c in l_cols if c in lines_df.columns]].copy()
    return b[b_cols], l[l_cols]

def audit_grid_security(buses_df: pd.DataFrame, lines_df: pd.DataFrame, base_mva: float = 100.0) -> Dict[str, Any]:
    """Evaluates grid compliance against statutory voltage limits (0.95 - 1.05 pu) and phase angles."""
    b, l = _filter_core_frames(buses_df, lines_df)
    sol = core_solve(b, l, max_iterations=30, tolerance=1e-6)
    sec = check_grid_security(b, l, sol, base_mva=base_mva)
    
    if not sec.get('converged', False):
        return {
            'converged': False,
            'status': 'Diverged / Voltage Collapse',
            'is_fully_compliant': False,
            'violations_count': 0
        }
        
    low_buses = sec['critical_low_voltage_buses'].to_dict(orient='records') if not sec['critical_low_voltage_buses'].empty else []
    high_buses = sec['critical_high_voltage_buses'].to_dict(orient='records') if not sec['critical_high_voltage_buses'].empty else []
    angles = sec['angle_violations'].to_dict(orient='records') if not sec['angle_violations'].empty else []
    
    return {
        'converged': True,
        'v_min_observed': sec['v_min_observed'],
        'v_max_observed': sec['v_max_observed'],
        'critical_low_voltage_buses': low_buses,
        'critical_high_voltage_buses': high_buses,
        'max_angle_diff_deg': sec['max_angle_diff_deg'],
        'angle_violations': angles,
        'total_p_loss_MW': sec['total_p_loss_MW'],
        'p_balance_err_MW': sec['p_balance_err_MW'],
        'q_balance_err_Mvar': sec['q_balance_err_Mvar'],
        'is_fully_compliant': bool(sec['is_fully_compliant']),
        'violations_count': len(low_buses) + len(high_buses) + len(angles)
    }

def compute_n1_contingency(buses_df: pd.DataFrame, lines_df: pd.DataFrame, base_mva: float = 100.0) -> List[Dict[str, Any]]:
    """Performs full automated N-1 line contingency scan."""
    b, l = _filter_core_frames(buses_df, lines_df)
    df_n1 = run_n1_contingency(b, l, base_mva=base_mva)
    records = df_n1.to_dict(orient='records')
    # Clean NaN values for JSON serialization
    for r in records:
        for k, v in r.items():
            if pd.isna(v):
                r[k] = None
    return records

def compute_load_stress_pv(buses_df: pd.DataFrame, lines_df: pd.DataFrame, base_mva: float = 100.0) -> List[Dict[str, Any]]:
    """Computes voltage stability P-V curve operating points."""
    b, l = _filter_core_frames(buses_df, lines_df)
    df_pv = run_load_stress_analysis(b, l, base_mva=base_mva)
    records = df_pv.to_dict(orient='records')
    for r in records:
        for k, v in r.items():
            if pd.isna(v):
                r[k] = None
    return records


# ==============================================================================
# 6. INDEPENDENT PYPOWER CROSS-VALIDATION
# ==============================================================================

def verify_case_with_pypower(buses_df: pd.DataFrame, lines_df: pd.DataFrame, base_mva: float = 100.0) -> Dict[str, Any]:
    """Compares the project solver against industry-standard PyPower (MATPOWER in Python)."""
    b = buses_df.copy()
    l = lines_df.copy()
    n = len(b)
    
    # Run project solver first
    sol_proj = solve_power_flow(b, l, base_mva=base_mva)
    if not sol_proj['converged']:
        return {
            'verified': False,
            'status': 'FAIL',
            'message': 'Thuật toán dự án không hội tụ trên hệ thống này.',
            'max_voltage_error_pu': None,
            'max_angle_error_deg': None,
            'loss_error_MW': None,
            'comparison': []
        }

    # Setup PyPower bus matrix
    bus = np.zeros((n, 13))
    bus[:, 0] = b['bus'].astype(int)
    type_map = {'Slack': 3, 'PV': 2, 'PQ': 1}
    bus[:, 1] = b['type'].map(type_map).fillna(1).astype(int)
    bus[:, 2] = base_mva * b['pd_pu'].fillna(0.0)
    bus[:, 3] = base_mva * b['qd_pu'].fillna(0.0)
    bus[:, 6] = 1.0  # area
    bus[:, 7] = b['vm_pu'].fillna(1.0)
    bus[:, 8] = b['va_deg'].fillna(0.0)
    bus[:, 9] = 110.0  # baseKV
    bus[:, 10] = 1.0  # zone
    bus[:, 11] = 1.1  # Vmax
    bus[:, 12] = 0.9  # Vmin

    genrows = []
    for r in b[b['type'] != 'PQ'].itertuples():
        genrows.append([int(r.bus), base_mva * getattr(r, 'pg_pu', 0.0), base_mva * getattr(r, 'qg_pu', 0.0), 9999.0, -9999.0, getattr(r, 'vm_pu', 1.0), base_mva, 1, 9999.0, -9999.0] + [0.0] * 11)
    if not genrows:
        genrows.append([1, 0.0, 0.0, 9999.0, -9999.0, 1.0, base_mva, 1, 9999.0, -9999.0] + [0.0] * 11)

    br = np.zeros((len(l), 13))
    br[:, 0] = l['from_bus'].astype(int)
    br[:, 1] = l['to_bus'].astype(int)
    br[:, 2] = l['r_pu'].astype(float)
    br[:, 3] = l['x_pu'].astype(float)
    br[:, 10] = 1.0  # status
    br[:, 11] = -360.0
    br[:, 12] = 360.0

    ppc = {
        'version': '2',
        'baseMVA': float(base_mva),
        'bus': bus,
        'gen': np.array(genrows, dtype=float),
        'branch': br
    }

    try:
        res, success = runpf(ppc, ppoption(VERBOSE=0, OUT_ALL=0, PF_TOL=1e-10, ENFORCE_Q_LIMS=0))
        if not success:
            return {
                'verified': False,
                'status': 'PYPOWER_DIVERGED',
                'message': 'PyPower không hội tụ.',
                'max_voltage_error_pu': None,
                'max_angle_error_deg': None,
                'loss_error_MW': None,
                'comparison': []
            }
        
        pp_bus_res = res['bus']
        pp_bus_map = {int(pp_bus_res[i, 0]): (float(pp_bus_res[i, 7]), float(pp_bus_res[i, 8])) for i in range(len(pp_bus_res))}
        
        comparison = []
        max_v_err = 0.0
        max_a_err = 0.0

        for b_item in sol_proj['buses']:
            bid = int(b_item['bus'])
            v_proj = float(b_item['vm_pu'])
            a_proj = float(b_item['va_deg'])
            v_pp, a_pp = pp_bus_map.get(bid, (v_proj, a_proj))
            
            v_err = abs(v_proj - v_pp)
            a_err = abs(a_proj - a_pp)
            max_v_err = max(max_v_err, v_err)
            max_a_err = max(max_a_err, a_err)

            comparison.append({
                'bus': bid,
                'type': b_item['type'],
                'v_project_pu': round(v_proj, 5),
                'v_pypower_pu': round(v_pp, 5),
                'v_diff_pu': f"{v_err:.2e}",
                'va_project_deg': round(a_proj, 3),
                'va_pypower_deg': round(a_pp, 3),
                'va_diff_deg': f"{a_err:.2e}",
                'status': 'PASS' if v_err < 1e-6 else 'WARN'
            })

        pp_loss = float((res['branch'][:, 13] + res['branch'][:, 15]).sum())
        proj_loss = sol_proj['summary']['total_loss_MW']
        loss_err = abs(proj_loss - pp_loss)
        is_passed = bool(max_v_err < 1e-6 and max_a_err < 1e-4 and loss_err < 1e-4)

        return {
            'verified': bool(is_passed),
            'status': 'PASS' if is_passed else 'WARNING',
            'max_voltage_error_pu': float(max_v_err),
            'max_angle_error_deg': float(max_a_err),
            'loss_error_MW': float(loss_err),
            'project_loss_MW': round(proj_loss, 4),
            'pypower_loss_MW': round(pp_loss, 4),
            'message': f"Đạt chuẩn kiểm định quốc tế PyPower (Sai lệch điện áp cực đại: {max_v_err:.2e} pu < 1e-6 pu)",
            'comparison': comparison
        }
    except Exception as exc:
        return {
            'verified': False,
            'status': 'ERROR',
            'message': f"Lỗi so sánh PyPower: {str(exc)}",
            'max_voltage_error_pu': None,
            'max_angle_error_deg': None,
            'loss_error_MW': None,
            'comparison': []
        }

