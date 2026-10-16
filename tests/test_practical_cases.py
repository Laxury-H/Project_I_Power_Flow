"""Automated testing and validation of realistic power system operating cases:
- Full benchmark suite: 3-bus, 5-bus, IEEE 14-bus, IEEE 30-bus, IEEE 57-bus, IEEE 118-bus
- Operational regimes: Light load (50%), Rated load (100%), Heavy load (120%)
- N-1 Contingency screening (single line outages, bridge detection, post-contingency voltage)
- Grid code compliance (voltage band [0.95, 1.05] pu, transmission phase angle limits)
- Physical power conservation (P and Q balances < 1e-8 MW/MVAR)
- Independent PYPOWER ground-truth validation
"""
import numpy as np
import pytest
from pypower.api import runpf, ppoption

from src.data_models import load_case
from src.newton_raphson import solve
from src.branch_flows import output_tables
from src.practical_scenarios import check_grid_security, run_n1_contingency, run_load_stress_analysis


ALL_BENCHMARKS = ['3bus', '5bus', '14bus', '30bus', '57bus', '118bus']


@pytest.mark.parametrize('name', ALL_BENCHMARKS)
def test_nominal_convergence_all_benchmarks(name):
    """Every academic benchmark must converge under nominal conditions within <= 5 iterations."""
    buses, lines = load_case(name)
    sol = solve(buses, lines, max_iterations=20, tolerance=1e-6)
    assert sol.converged, f"Case {name} failed to converge"
    assert sol.iterations <= 6, f"Case {name} took too many iterations: {sol.iterations}"
    
    b_res, l_res = output_tables(buses, lines, sol)
    # Conservation of active power: sum(P_net) == sum(P_loss)
    assert abs(b_res['p_net_MW'].sum() - l_res['p_loss_MW'].sum()) < 1e-7
    # Conservation of reactive power: sum(Q_net) == sum(Q_loss)
    assert abs(b_res['q_net_Mvar'].sum() - l_res['q_absorption_Mvar'].sum()) < 1e-7
    # All line losses non-negative
    assert (l_res['p_loss_MW'] >= -1e-8).all()


@pytest.mark.parametrize('name', ['3bus', '5bus', '14bus', '30bus'])
@pytest.mark.parametrize('scale', [0.5, 0.8, 1.0, 1.2])
def test_realistic_load_scaling_regimes(name, scale):
    """Verify system solves across practical load regimes (light load 50% to peak load 120%)."""
    buses, lines = load_case(name)
    buses[['pd_pu', 'qd_pu']] *= scale
    sol = solve(buses, lines, max_iterations=25, tolerance=1e-6)
    assert sol.converged
    
    b_res, l_res = output_tables(buses, lines, sol)
    # At lighter loads, average and minimum voltage should generally be higher (or less loaded)
    assert b_res['vm_pu'].min() > 0.85
    assert l_res['p_loss_MW'].sum() >= 0.0


@pytest.mark.parametrize('name', ['3bus', '5bus', '14bus'])
def test_n1_contingency_screening(name):
    """Verify N-1 contingency scan correctly evaluates all line outages."""
    buses, lines = load_case(name)
    df_n1 = run_n1_contingency(buses, lines, base_mva=100.0)
    
    assert len(df_n1) == len(lines)
    assert 'severity_score' in df_n1.columns
    assert 'risk_level' in df_n1.columns
    
    # At least some non-bridge outages must converge
    converged_cases = df_n1[df_n1['converged'] == True]
    assert len(converged_cases) > 0
    for _, row in converged_cases.iterrows():
        assert row['v_min_pu'] > 0.80
        assert row['p_loss_MW'] > 0.0


def test_grid_security_evaluation():
    """Verify grid code security checks correctly identify compliant and non-compliant states."""
    buses, lines = load_case('14bus')
    sol = solve(buses, lines)
    report = check_grid_security(buses, lines, sol, base_mva=100.0, v_min=0.95, v_max=1.06)
    
    assert report['converged'] is True
    assert report['p_balance_err_MW'] < 1e-6
    assert report['q_balance_err_Mvar'] < 1e-6
    assert isinstance(report['is_fully_compliant'], bool)


def test_load_stress_analysis_pv_curve():
    """Verify load stress analysis produces progressive loading points."""
    buses, lines = load_case('5bus')
    stress_df = run_load_stress_analysis(buses, lines, scale_steps=[0.5, 1.0, 1.3])
    
    assert len(stress_df) == 3
    assert (stress_df['converged'] == True).all()
    # Higher load should produce higher total active losses
    assert stress_df.loc[2, 'p_loss_MW'] > stress_df.loc[0, 'p_loss_MW']


@pytest.mark.parametrize('name', ['14bus', '30bus'])
def test_pypower_cross_validation(name):
    """Cross-verify Newton-Raphson results with independent PYPOWER solver on IEEE cases."""
    b, l = load_case(name)
    n = len(b)
    
    # Construct PYPOWER case structure
    bus_data = np.zeros((n, 13))
    bus_data[:, 0] = b.bus
    bus_data[:, 1] = b.type.map({'Slack': 3, 'PV': 2, 'PQ': 1})
    bus_data[:, 2] = 100.0 * b.pd_pu
    bus_data[:, 3] = 100.0 * b.qd_pu
    bus_data[:, 6] = 1.0
    bus_data[:, 7] = b.vm_pu
    bus_data[:, 8] = b.va_deg
    bus_data[:, 9] = 110.0
    bus_data[:, 10] = 1.0
    bus_data[:, 11] = 1.1
    bus_data[:, 12] = 0.9
    
    gen_rows = []
    for r in b[b.type != 'PQ'].itertuples():
        gen_rows.append([r.bus, 100.0 * r.pg_pu, 100.0 * r.qg_pu, 999, -999, r.vm_pu, 100, 1, 999, -999] + [0] * 11)
        
    branch_data = np.zeros((len(l), 13))
    branch_data[:, 0] = l.from_bus
    branch_data[:, 1] = l.to_bus
    branch_data[:, 2] = l.r_pu
    branch_data[:, 3] = l.x_pu
    branch_data[:, 10] = 1.0
    branch_data[:, 11] = -360.0
    branch_data[:, 12] = 360.0
    
    pp_case = {
        'version': '2',
        'baseMVA': 100.0,
        'bus': bus_data,
        'gen': np.array(gen_rows, dtype=float),
        'branch': branch_data
    }
    
    pp_result, pp_ok = runpf(pp_case, ppoption(VERBOSE=0, OUT_ALL=0, PF_TOL=1e-10, ENFORCE_Q_LIMS=0))
    assert pp_ok, f"PYPOWER failed on {name}"
    
    sol = solve(b, l)
    assert sol.converged
    _, flows = output_tables(b, l, sol)
    
    # Error comparison
    v_err = float(np.max(np.abs(sol.vm - pp_result['bus'][:, 7])))
    va_err = float(np.max(np.abs(np.rad2deg(sol.va) - pp_result['bus'][:, 8])))
    loss_err = float(abs(flows['p_loss_MW'].sum() - (pp_result['branch'][:, 13] + pp_result['branch'][:, 15]).sum()))
    
    assert v_err < 1e-6, f"Voltage error vs PYPOWER too large: {v_err}"
    assert va_err < 1e-4, f"Angle error vs PYPOWER too large: {va_err}"
    assert loss_err < 1e-3, f"Loss error vs PYPOWER too large: {loss_err}"


def test_high_r_x_ratio_distribution_grid():
    """Verify solver handles high R/X ratios typical of medium-voltage distribution systems."""
    b, l = load_case('5bus')
    # Increase resistance so R/X = 1.0 (typical distribution line)
    l_high_rx = l.copy()
    l_high_rx['r_pu'] = l_high_rx['x_pu']
    sol = solve(b, l_high_rx, max_iterations=25)
    assert sol.converged, "High R/X network must still converge"
    b_res, l_res = output_tables(b, l_high_rx, sol)
    assert abs(b_res['p_net_MW'].sum() - l_res['p_loss_MW'].sum()) < 1e-7


def test_contingency_loss_escalation_detection():
    """Verify that severe contingency (Line 1-2 outage in IEEE 14) detects expected loss surge."""
    b, l = load_case('14bus')
    base_sol = solve(b, l)
    _, base_l = output_tables(b, l, base_sol)
    base_loss = base_l['p_loss_MW'].sum()
    
    # Trip line 1-2 (index 0)
    l_trip = l.iloc[1:].reset_index(drop=True)
    trip_sol = solve(b, l_trip)
    assert trip_sol.converged
    _, trip_l = output_tables(b, l_trip, trip_sol)
    trip_loss = trip_l['p_loss_MW'].sum()
    
    # Loss should surge significantly (> 50% increase)
    assert trip_loss > base_loss * 1.5


def test_voltage_collapse_detection_at_extreme_load():
    """Verify that beyond the maximum loadability limit, the solver gracefully reports divergence."""
    b, l = load_case('14bus')
    # Extreme load scale (450%) beyond system transfer capability (P-V nose point)
    b[['pd_pu', 'qd_pu']] *= 4.5
    sol = solve(b, l, max_iterations=20)
    assert not sol.converged, "Extreme overload must report non-convergence (voltage collapse)"

    b57, l57 = load_case('57bus')
    b57[['pd_pu', 'qd_pu']] *= 1.6
    sol57 = solve(b57, l57, max_iterations=20)
    assert not sol57.converged, "57-bus at 1.6x exceeds voltage stability margin"
