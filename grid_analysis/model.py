from dataclasses import dataclass
import pandas as pd

BUS_COLUMNS = {"bus", "load_mw", "generation_mw", "is_slack"}
LINE_COLUMNS = {"line", "from_bus", "to_bus", "reactance_pu", "limit_mw"}

@dataclass
class GridCase:
    buses: pd.DataFrame
    lines: pd.DataFrame
    name: str = "Synthetic 9-bus network"

    def validate(self):
        missing_bus = BUS_COLUMNS - set(self.buses.columns)
        missing_line = LINE_COLUMNS - set(self.lines.columns)
        if missing_bus:
            raise ValueError(f"Bus table is missing columns: {sorted(missing_bus)}")
        if missing_line:
            raise ValueError(f"Line table is missing columns: {sorted(missing_line)}")
        if self.buses.empty or self.lines.empty:
            raise ValueError("The network must contain buses and lines.")
        if self.buses["bus"].duplicated().any():
            raise ValueError("Bus identifiers must be unique.")
        if self.lines["line"].duplicated().any():
            raise ValueError("Line identifiers must be unique.")
        if int(self.buses["is_slack"].sum()) != 1:
            raise ValueError("Exactly one slack bus is required.")
        bus_ids = set(self.buses["bus"])
        if not set(self.lines["from_bus"]).issubset(bus_ids) or not set(self.lines["to_bus"]).issubset(bus_ids):
            raise ValueError("Every line endpoint must reference an existing bus.")
        if (self.lines["from_bus"] == self.lines["to_bus"]).any():
            raise ValueError("A line cannot connect a bus to itself.")
        if (self.lines["reactance_pu"] <= 0).any():
            raise ValueError("Line reactance must be positive.")
        if (self.lines["limit_mw"] <= 0).any():
            raise ValueError("Line limits must be positive.")
        if (self.buses[["load_mw", "generation_mw"]] < 0).any().any():
            raise ValueError("Loads and scheduled generation must be non-negative.")

    @property
    def slack_bus(self):
        self.validate()
        return int(self.buses.loc[self.buses["is_slack"], "bus"].iloc[0])
