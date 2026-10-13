import pandas as pd
from .solver import solve_power_flow
from .model import GridCase

def run_n1_analysis(case: GridCase, load_multiplier=1.0):
    rows = []
    for outage in case.lines["line"].tolist():
        try:
            _, lines, diag = solve_power_flow(case, load_multiplier, outage)
            rows.append({
                "outaged_line": outage,
                "status": "OK",
                "overloaded_line_count": int(lines["overloaded"].sum()),
                "max_loading_pct": float(lines["loading_pct"].max()),
                "total_overload_pct": float((lines["loading_pct"] - 100).clip(lower=0).sum()),
                "slack_injection_mw": diag["slack_injection_mw"],
            })
        except ValueError as exc:
            rows.append({
                "outaged_line": outage,
                "status": f"INFEASIBLE: {exc}",
                "overloaded_line_count": -1,
                "max_loading_pct": float("inf"),
                "total_overload_pct": float("inf"),
                "slack_injection_mw": float("nan"),
            })
    result = pd.DataFrame(rows)
    return result.sort_values(
        ["overloaded_line_count", "total_overload_pct", "max_loading_pct"],
        ascending=[False, False, False], kind="stable"
    ).reset_index(drop=True)
