import pandas as pd
from .solver import solve_power_flow
from .model import GridCase

def evaluate_load_growth(case: GridCase, multipliers=(1.0, 1.1, 1.2, 1.3, 1.4, 1.5)):
    rows = []
    for multiplier in multipliers:
        _, lines, diag = solve_power_flow(case, load_multiplier=float(multiplier))
        rows.append({
            "load_multiplier": float(multiplier),
            "demand_growth_pct": 100 * (float(multiplier) - 1),
            "total_load_mw": diag["total_load_mw"],
            "slack_injection_mw": diag["slack_injection_mw"],
            "max_line_loading_pct": float(lines["loading_pct"].max()),
            "overloaded_line_count": int(lines["overloaded"].sum()),
            "power_balance_error_mw": diag["power_balance_error_mw"],
        })
    return pd.DataFrame(rows)
