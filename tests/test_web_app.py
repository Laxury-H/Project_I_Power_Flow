"""
Unit and integration tests for the web_app service and backend logic.
Verifies:
- 3-bus and 5-bus benchmark cases solving
- Input validation (missing slack, duplicate slack, disconnected network, non-positive X)
- Y-bus matrix calculation
- Q-limit violation detection
- System power balance conservation
"""

import pandas as pd
import pytest

from web_app.backend.solver_service import (
    validate_grid_data,
    compute_ybus_matrix,
    solve_power_flow,
    PRESETS
)


def test_preset_3bus_solve():
    preset = PRESETS['3bus']
    df_b = pd.DataFrame(preset['buses'])
    df_l = pd.DataFrame(preset['lines'])
    
    val = validate_grid_data(preset['buses'], preset['lines'])
    assert val['valid'] is True
    assert val['slack_count'] == 1

    ybus = compute_ybus_matrix(df_b, df_l)
    assert ybus['dim'] == 3
    assert ybus['non_zeros'] == 9

    sol = solve_power_flow(df_b, df_l, base_mva=100.0, tolerance=1e-6)
    assert sol['converged'] is True
    assert sol['iterations'] <= 4
    assert abs(sol['buses'][2]['vm_pu'] - 0.9844) < 1e-3
    assert abs(sol['summary']['total_loss_MW'] - 2.2047) < 1e-2
    assert sol['summary']['p_balance_error_MW'] < 1e-8


def test_preset_5bus_solve():
    preset = PRESETS['5bus']
    df_b = pd.DataFrame(preset['buses'])
    df_l = pd.DataFrame(preset['lines'])
    
    val = validate_grid_data(preset['buses'], preset['lines'])
    assert val['valid'] is True

    sol = solve_power_flow(df_b, df_l, base_mva=100.0, tolerance=1e-6)
    assert sol['converged'] is True
    assert sol['iterations'] <= 5
    assert abs(sol['summary']['total_loss_MW'] - 3.6505) < 1e-2


def test_validation_two_slacks_rejected():
    preset = PRESETS['3bus']
    buses = [dict(b) for b in preset['buses']]
    buses[1]['type'] = 'Slack'
    val = validate_grid_data(buses, preset['lines'])
    assert val['valid'] is False
    assert any("2 nút Slack" in err or "nhiều hơn 1" in err for err in val['errors'])


def test_validation_missing_slack_rejected():
    preset = PRESETS['3bus']
    buses = [dict(b) for b in preset['buses']]
    buses[0]['type'] = 'PQ'
    val = validate_grid_data(buses, preset['lines'])
    assert val['valid'] is False
    assert any("chưa có nút cân bằng" in err for err in val['errors'])


def test_validation_disconnected_network_rejected():
    preset = PRESETS['3bus']
    # Only line 1-2, leaving bus 3 disconnected
    isolated_lines = [{'from_bus': 1, 'to_bus': 2, 'r_pu': 0.02, 'x_pu': 0.06}]
    val = validate_grid_data(preset['buses'], isolated_lines)
    assert val['valid'] is False
    assert any("chia cắt" in err or "cô lập" in err for err in val['errors'])
    assert 3 in val['islanded_buses']


def test_validation_invalid_impedance_rejected():
    preset = PRESETS['3bus']
    lines = [dict(l) for l in preset['lines']]
    lines[0]['x_pu'] = -0.05
    val = validate_grid_data(preset['buses'], lines)
    assert val['valid'] is False
    assert any("Điện kháng X" in err for err in val['errors'])


def test_all_presets_meta():
    from web_app.backend.solver_service import get_all_presets_meta, get_preset_case
    meta_list = get_all_presets_meta()
    assert len(meta_list) == 6
    ids = [m['id'] for m in meta_list]
    assert '14bus' in ids and '30bus' in ids and '118bus' in ids

    case14 = get_preset_case('14bus')
    assert len(case14['buses']) == 14
    assert len(case14['lines']) == 20


def test_audit_grid_security():
    from web_app.backend.solver_service import audit_grid_security, get_preset_case
    c = get_preset_case('3bus')
    df_b = pd.DataFrame(c['buses'])
    df_l = pd.DataFrame(c['lines'])
    sec = audit_grid_security(df_b, df_l, base_mva=100.0)
    assert sec['converged'] is True
    assert sec['v_min_observed'] > 0.95
    assert sec['is_fully_compliant'] is True


def test_contingency_n1():
    from web_app.backend.solver_service import compute_n1_contingency, get_preset_case
    c = get_preset_case('5bus')
    df_b = pd.DataFrame(c['buses'])
    df_l = pd.DataFrame(c['lines'])
    n1 = compute_n1_contingency(df_b, df_l, base_mva=100.0)
    assert len(n1) == 7
    assert any(item['converged'] is True for item in n1)


def test_load_stress_pv():
    from web_app.backend.solver_service import compute_load_stress_pv, get_preset_case
    c = get_preset_case('3bus')
    df_b = pd.DataFrame(c['buses'])
    df_l = pd.DataFrame(c['lines'])
    pv = compute_load_stress_pv(df_b, df_l, base_mva=100.0)
    assert len(pv) >= 5
    assert pv[0]['converged'] is True


def test_verify_case_with_pypower():
    from web_app.backend.solver_service import verify_case_with_pypower, get_preset_case
    c = get_preset_case('3bus')
    df_b = pd.DataFrame(c['buses'])
    df_l = pd.DataFrame(c['lines'])
    comp = verify_case_with_pypower(df_b, df_l, base_mva=100.0)
    assert comp['verified'] is True
    assert comp['status'] == 'PASS'
    assert comp['max_voltage_error_pu'] < 1e-6
    assert len(comp['comparison']) == 3

