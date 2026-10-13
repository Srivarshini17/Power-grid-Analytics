import numpy as np
import pandas as pd
import networkx as nx
from .model import GridCase

def check_connected(case: GridCase, outaged_line=None):
    graph = nx.Graph()
    graph.add_nodes_from(case.buses["bus"].astype(int).tolist())
    for row in case.lines.itertuples(index=False):
        if row.line != outaged_line:
            graph.add_edge(int(row.from_bus), int(row.to_bus))
    if not nx.is_connected(graph):
        raise ValueError(f"Network is disconnected after outage {outaged_line!r}.")

def build_susceptance_matrix(case: GridCase, outaged_line=None):
    case.validate()
    check_connected(case, outaged_line)
    bus_ids = case.buses["bus"].astype(int).tolist()
    position = {bus: i for i, bus in enumerate(bus_ids)}
    B = np.zeros((len(bus_ids), len(bus_ids)), dtype=float)
    active_lines = case.lines[case.lines["line"] != outaged_line].copy()
    for row in active_lines.itertuples(index=False):
        i, j = position[int(row.from_bus)], position[int(row.to_bus)]
        susceptance = 1.0 / float(row.reactance_pu)
        B[i, i] += susceptance
        B[j, j] += susceptance
        B[i, j] -= susceptance
        B[j, i] -= susceptance
    return B, bus_ids, active_lines

def solve_power_flow(case: GridCase, load_multiplier=1.0, outaged_line=None):
    if load_multiplier < 0:
        raise ValueError("Load multiplier must be non-negative.")
    B, bus_ids, active_lines = build_susceptance_matrix(case, outaged_line)
    buses = case.buses.copy()
    buses["load_mw"] *= load_multiplier
    slack_bus = case.slack_bus
    slack_index = bus_ids.index(slack_bus)
    other_indices = [i for i, bus in enumerate(bus_ids) if bus != slack_bus]

    # Positive net injection means generation minus load.
    injection = buses["generation_mw"].to_numpy(float) - buses["load_mw"].to_numpy(float)
    # Slack bus balances the scheduled injections at all non-slack buses.
    injection[slack_index] = -injection[other_indices].sum()

    reduced_B = B[np.ix_(other_indices, other_indices)]
    try:
        theta_other = np.linalg.solve(reduced_B, injection[other_indices])
    except np.linalg.LinAlgError as exc:
        raise ValueError("Power-flow matrix is singular; check network connectivity.") from exc

    theta = np.zeros(len(bus_ids))
    theta[other_indices] = theta_other
    angle_deg = np.degrees(theta)

    bus_results = buses[["bus", "load_mw", "generation_mw", "is_slack"]].copy()
    bus_results["net_injection_mw"] = injection
    bus_results["angle_rad"] = theta
    bus_results["angle_deg"] = angle_deg

    pos = {bus: i for i, bus in enumerate(bus_ids)}
    line_results = active_lines.copy()
    line_results["flow_mw"] = [
        (theta[pos[int(row.from_bus)]] - theta[pos[int(row.to_bus)]]) / float(row.reactance_pu)
        for row in line_results.itertuples(index=False)
    ]
    line_results["absolute_flow_mw"] = line_results["flow_mw"].abs()
    line_results["loading_pct"] = 100 * line_results["absolute_flow_mw"] / line_results["limit_mw"]
    line_results["overloaded"] = line_results["loading_pct"] > 100

    diagnostics = {
        "slack_bus": slack_bus,
        "slack_injection_mw": float(injection[slack_index]),
        "total_load_mw": float(buses["load_mw"].sum()),
        "max_abs_angle_deg": float(np.max(np.abs(angle_deg))),
        "matrix_condition_number": float(np.linalg.cond(reduced_B)),
        "power_balance_error_mw": float(injection.sum()),
        "outaged_line": outaged_line,
    }
    return bus_results, line_results, diagnostics
