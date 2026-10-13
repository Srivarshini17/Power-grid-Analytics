import numpy as np
import pytest
from grid_analysis.sample_network import make_sample_case
from grid_analysis.solver import solve_power_flow, build_susceptance_matrix
from grid_analysis.contingency import run_n1_analysis
from grid_analysis.scenarios import evaluate_load_growth

def test_base_case_balances_power_and_has_finite_results():
    buses, lines, diag = solve_power_flow(make_sample_case())
    assert abs(diag["power_balance_error_mw"]) < 1e-8
    assert np.isfinite(buses["angle_deg"]).all()
    assert np.isfinite(lines["flow_mw"]).all()
    assert len(buses) == 9 and len(lines) == 11

def test_line_flow_matches_angle_equation():
    buses, lines, _ = solve_power_flow(make_sample_case())
    angle = dict(zip(buses["bus"], buses["angle_rad"]))
    for row in lines.itertuples():
        expected = (angle[row.from_bus] - angle[row.to_bus]) / row.reactance_pu
        assert row.flow_mw == pytest.approx(expected)

def test_n1_analysis_checks_every_line():
    case = make_sample_case()
    result = run_n1_analysis(case)
    assert len(result) == len(case.lines)
    assert result["outaged_line"].nunique() == len(case.lines)

def test_demand_scenarios_increase_total_load():
    result = evaluate_load_growth(make_sample_case(), (1.0, 1.1, 1.2))
    assert result["demand_growth_pct"].tolist() == pytest.approx([0.0, 10.0, 20.0])
    assert (result["total_load_mw"].diff().dropna() > 0).all()

def test_invalid_reactance_is_rejected():
    case = make_sample_case()
    case.lines.loc[0, "reactance_pu"] = 0
    with pytest.raises(ValueError, match="reactance"):
        build_susceptance_matrix(case)

def test_invalid_slack_count_is_rejected():
    case = make_sample_case()
    case.buses["is_slack"] = False
    with pytest.raises(ValueError, match="slack"):
        case.validate()
