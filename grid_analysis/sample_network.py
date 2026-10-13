import pandas as pd
from .model import GridCase

def make_sample_case():
    # Synthetic example. Values are illustrative, not measured grid data.
    buses = pd.DataFrame([
        {"bus": 1, "load_mw": 0.,  "generation_mw": 0.,  "is_slack": True},
        {"bus": 2, "load_mw": 20., "generation_mw": 55., "is_slack": False},
        {"bus": 3, "load_mw": 45., "generation_mw": 45., "is_slack": False},
        {"bus": 4, "load_mw": 20., "generation_mw": 0.,  "is_slack": False},
        {"bus": 5, "load_mw": 60., "generation_mw": 0.,  "is_slack": False},
        {"bus": 6, "load_mw": 25., "generation_mw": 0.,  "is_slack": False},
        {"bus": 7, "load_mw": 35., "generation_mw": 0.,  "is_slack": False},
        {"bus": 8, "load_mw": 50., "generation_mw": 0.,  "is_slack": False},
        {"bus": 9, "load_mw": 30., "generation_mw": 0.,  "is_slack": False},
    ])
    lines = pd.DataFrame([
        {"line": "L1-4", "from_bus": 1, "to_bus": 4, "reactance_pu": .0576, "limit_mw": 100.},
        {"line": "L4-5", "from_bus": 4, "to_bus": 5, "reactance_pu": .0920, "limit_mw": 80.},
        {"line": "L5-6", "from_bus": 5, "to_bus": 6, "reactance_pu": .1700, "limit_mw": 60.},
        {"line": "L3-6", "from_bus": 3, "to_bus": 6, "reactance_pu": .0586, "limit_mw": 90.},
        {"line": "L6-7", "from_bus": 6, "to_bus": 7, "reactance_pu": .1000, "limit_mw": 65.},
        {"line": "L7-8", "from_bus": 7, "to_bus": 8, "reactance_pu": .0720, "limit_mw": 70.},
        {"line": "L8-2", "from_bus": 8, "to_bus": 2, "reactance_pu": .0625, "limit_mw": 100.},
        {"line": "L8-9", "from_bus": 8, "to_bus": 9, "reactance_pu": .1610, "limit_mw": 55.},
        {"line": "L9-4", "from_bus": 9, "to_bus": 4, "reactance_pu": .0850, "limit_mw": 75.},
        {"line": "L2-7", "from_bus": 2, "to_bus": 7, "reactance_pu": .1000, "limit_mw": 75.},
        {"line": "L2-3", "from_bus": 2, "to_bus": 3, "reactance_pu": .0800, "limit_mw": 80.},
    ])
    case = GridCase(buses, lines)
    case.validate()
    return case
