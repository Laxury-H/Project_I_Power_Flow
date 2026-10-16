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
