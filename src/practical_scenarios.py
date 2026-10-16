"""Practical operational scenario analysis and N-1 contingency screening for power systems."""
import numpy as np
import pandas as pd
from .validation import validate
from .newton_raphson import solve
from .branch_flows import output_tables


def check_grid_security(buses, lines, solution, base_mva=100.0, v_min=0.95, v_max=1.05, max_angle_diff_deg=30.0):
    """Assess power system state against realistic grid code standards.
    
    Checks:
    - Bus voltage compliance within [v_min, v_max] pu (IEEE / EVN grid code)
    - Transmission line voltage angle differences <= max_angle_diff_deg (stability limit)
    - Active and reactive power conservation balance
    """
    if not solution.converged:
        return {'converged': False, 'status': 'Diverged / Voltage Collapse'}
    
    bus_results, branch_results = output_tables(buses, lines, solution, base_mva)
    
    # Voltage violations
    low_v = bus_results[bus_results['vm_pu'] < v_min][['bus', 'type', 'vm_pu']].copy()
    high_v = bus_results[bus_results['vm_pu'] > v_max][['bus', 'type', 'vm_pu']].copy()
    
    # Phase angle differences across lines
    va_map = dict(zip(bus_results['bus'], bus_results['va_deg']))
    angle_diffs = []
    for r in lines.itertuples():
        diff = abs(va_map[r.from_bus] - va_map[r.to_bus])
        angle_diffs.append(diff)
    
    max_angle_diff = max(angle_diffs) if angle_diffs else 0.0
    critical_angles = []
    for idx, r in enumerate(lines.itertuples()):
        diff = angle_diffs[idx]
        if diff > max_angle_diff_deg:
            critical_angles.append({
                'from_bus': int(r.from_bus),
                'to_bus': int(r.to_bus),
                'angle_diff_deg': float(diff)
            })
    
    # Power conservation checks
    p_gen = bus_results['pg_MW'].sum()
    p_load = bus_results['pd_MW'].sum()
    p_loss = branch_results['p_loss_MW'].sum()
    p_balance_err = abs(p_gen - p_load - p_loss)
    
    q_gen = bus_results['qg_Mvar'].sum()
    q_load = bus_results['qd_Mvar'].sum()
    q_loss = branch_results['q_absorption_Mvar'].sum()
    q_balance_err = abs(q_gen - q_load - q_loss)
    
    return {
        'converged': True,
        'v_min_observed': float(bus_results['vm_pu'].min()),
        'v_max_observed': float(bus_results['vm_pu'].max()),
        'critical_low_voltage_buses': low_v,
        'critical_high_voltage_buses': high_v,
        'max_angle_diff_deg': float(max_angle_diff),
        'angle_violations': pd.DataFrame(critical_angles),
        'total_p_loss_MW': float(p_loss),
        'p_balance_err_MW': float(p_balance_err),
        'q_balance_err_Mvar': float(q_balance_err),
        'is_fully_compliant': (len(low_v) == 0 and len(high_v) == 0 and len(critical_angles) == 0)
    }


def run_n1_contingency(buses, lines, base_mva=100.0, max_iterations=25, tolerance=1e-6):
    """Execute an automated N-1 contingency scan over all transmission lines.
    
    For each line, tests disconnection (outage):
    - Identifies if outage creates an isolated bus (network islanding)
    - If connected, solves post-contingency AC power flow
    - Computes post-contingency lowest bus voltage, total system losses, and severity index
    - Ranks contingencies by risk level
    """
    records = []
    
    # Base case reference
    base_sol = solve(buses, lines, max_iterations=max_iterations, tolerance=tolerance)
    base_loss = 0.0
    if base_sol.converged:
        _, base_br = output_tables(buses, lines, base_sol, base_mva)
        base_loss = float(base_br['p_loss_MW'].sum())
    
    for idx, row in lines.iterrows():
        fb = int(row['from_bus'])
        tb = int(row['to_bus'])
        line_desc = f"{fb} ➜ {tb}"
        
        rem_lines = lines.drop(index=idx).reset_index(drop=True)
        
        # Test topology connectivity
        try:
            validate(buses, rem_lines)
        except ValueError as exc:
            records.append({
                'line_id': idx + 1,
                'outage': line_desc,
                'status': '⚠️ Phân đảo lưới (Islanded)',
                'converged': False,
                'iterations': 0,
                'v_min_pu': np.nan,
                'worst_bus': 'N/A',
                'p_loss_MW': np.nan,
                'loss_delta_MW': np.nan,
                'voltage_violations': np.nan,
                'severity_score': 999.0,
                'risk_level': '🔴 Cực kỳ nghiêm trọng (Mất liên lạc)'
            })
            continue
            
        # Run AC Power Flow
        try:
            sol = solve(buses, rem_lines, max_iterations=max_iterations, tolerance=tolerance)
            if sol.converged:
                b_res, l_res = output_tables(buses, rem_lines, sol, base_mva)
                vmin = float(b_res['vm_pu'].min())
                worst_bus_id = int(b_res.loc[b_res['vm_pu'].idxmin(), 'bus'])
                ploss = float(l_res['p_loss_MW'].sum())
                delta_loss = ploss - base_loss
                
                # Count voltage violations (< 0.95 or > 1.05)
                v_violations = int(((b_res['vm_pu'] < 0.95) | (b_res['vm_pu'] > 1.05)).sum())
                
                # Severity Index (SI): quadratic voltage penalty + normalized loss increase
                v_penalty = float(((np.maximum(0.95 - b_res['vm_pu'], 0) / 0.05)**2).sum())
                severity = round(v_penalty * 10.0 + max(0.0, delta_loss) / max(1.0, base_loss), 3)
                
                if vmin < 0.90 or v_violations >= 3:
                    risk = '🔴 Nghiêm trọng (Sụt áp nặng)'
                elif vmin < 0.95 or v_violations > 0:
                    risk = '🟡 Cảnh báo (Vi phạm điện áp)'
                else:
                    risk = '🟢 An toàn (Đạt chuẩn N-1)'
                    
                records.append({
                    'line_id': idx + 1,
                    'outage': line_desc,
                    'status': f'✅ Hội tụ ({sol.iterations} iters)',
                    'converged': True,
                    'iterations': sol.iterations,
                    'v_min_pu': round(vmin, 4),
                    'worst_bus': f'Bus {worst_bus_id}',
                    'p_loss_MW': round(ploss, 3),
                    'loss_delta_MW': round(delta_loss, 3),
                    'voltage_violations': v_violations,
                    'severity_score': severity,
                    'risk_level': risk
                })
            else:
                records.append({
                    'line_id': idx + 1,
                    'outage': line_desc,
                    'status': '❌ Sụp đổ điện áp (Diverged)',
                    'converged': False,
                    'iterations': sol.iterations,
                    'v_min_pu': np.nan,
                    'worst_bus': 'N/A',
                    'p_loss_MW': np.nan,
                    'loss_delta_MW': np.nan,
                    'voltage_violations': np.nan,
                    'severity_score': 500.0,
                    'risk_level': '🔴 Không hội tụ (Mất cân bằng)'
                })
        except Exception as e:
            records.append({
                'line_id': idx + 1,
                'outage': line_desc,
                'status': f'Lỗi: {str(e)[:30]}',
                'converged': False,
                'iterations': 0,
                'v_min_pu': np.nan,
                'worst_bus': 'N/A',
                'p_loss_MW': np.nan,
                'loss_delta_MW': np.nan,
                'voltage_violations': np.nan,
                'severity_score': 800.0,
                'risk_level': '🔴 Lỗi tính toán'
            })
            
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values(by='severity_score', ascending=False).reset_index(drop=True)
    return df


def run_load_stress_analysis(buses, lines, scale_steps=None, base_mva=100.0, max_iterations=25):
    """Calculate P-V curve points across realistic load scaling regimes (30% to 180%).
    
    Identifies the voltage collapse threshold and loading margin.
    """
    if scale_steps is None:
        scale_steps = [0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
        
    records = []
    base_load = float(buses['pd_pu'].sum() * base_mva)
    
    for sc in scale_steps:
        b_sc = buses.copy()
        b_sc[['pd_pu', 'qd_pu']] = b_sc[['pd_pu', 'qd_pu']] * sc
        total_p_demand = base_load * sc
        
        try:
            sol = solve(b_sc, lines, max_iterations=max_iterations)
            if sol.converged:
                b_res, l_res = output_tables(b_sc, lines, sol, base_mva)
                vmin = float(b_res['vm_pu'].min())
                worst_bus = int(b_res.loc[b_res['vm_pu'].idxmin(), 'bus'])
                ploss = float(l_res['p_loss_MW'].sum())
                records.append({
                    'scale_pct': int(round(sc * 100)),
                    'demand_MW': round(total_p_demand, 2),
                    'converged': True,
                    'iterations': sol.iterations,
                    'v_min_pu': round(vmin, 4),
                    'worst_bus': f'Bus {worst_bus}',
                    'p_loss_MW': round(ploss, 3),
                    'status': '✅ Hội tụ'
                })
            else:
                records.append({
                    'scale_pct': int(round(sc * 100)),
                    'demand_MW': round(total_p_demand, 2),
                    'converged': False,
                    'iterations': sol.iterations,
                    'v_min_pu': np.nan,
                    'worst_bus': 'N/A',
                    'p_loss_MW': np.nan,
                    'status': '❌ Sụp đổ điện áp (Diverged)'
                })
        except Exception:
            records.append({
                'scale_pct': int(round(sc * 100)),
                'demand_MW': round(total_p_demand, 2),
                'converged': False,
                'iterations': 0,
                'v_min_pu': np.nan,
                'worst_bus': 'N/A',
                'p_loss_MW': np.nan,
                'status': '❌ Lỗi phân tích'
            })
            
    return pd.DataFrame(records)
