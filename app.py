import streamlit as st
from grid_analysis.sample_network import make_sample_case
from grid_analysis.solver import solve_power_flow
from grid_analysis.contingency import run_n1_analysis
from grid_analysis.scenarios import evaluate_load_growth

st.set_page_config(page_title="Power Grid Analytics", page_icon="⚡", layout="wide")
st.title("⚡ Power Grid Analytics & Contingency Planning")
st.caption("Educational DC power-flow approximation using a synthetic network. Not for operational decisions.")
case = make_sample_case()

with st.sidebar:
    st.header("Scenario controls")
    growth = st.slider("Demand growth (%)", 0, 50, 0, 5)
    outage = st.selectbox("Line outage", ["None"] + case.lines["line"].tolist())

try:
    buses, lines, diag = solve_power_flow(case, 1 + growth / 100, None if outage == "None" else outage)
    contingencies = run_n1_analysis(case, 1 + growth / 100)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total demand", f"{diag['total_load_mw']:.1f} MW")
    c2.metric("Slack injection", f"{diag['slack_injection_mw']:.1f} MW")
    c3.metric("Maximum line loading", f"{lines['loading_pct'].max():.1f}%")
    c4.metric("Overloaded lines", int(lines["overloaded"].sum()))
    left, right = st.columns(2)
    with left:
        st.subheader("Bus angles")
        st.dataframe(buses[["bus", "load_mw", "net_injection_mw", "angle_deg"]].round(4), use_container_width=True, hide_index=True)
    with right:
        st.subheader("Line flows and loading")
        st.dataframe(lines[["line", "from_bus", "to_bus", "flow_mw", "limit_mw", "loading_pct", "overloaded"]].round(2), use_container_width=True, hide_index=True)
    st.subheader("N-1 contingency ranking")
    st.dataframe(contingencies.round(2), use_container_width=True, hide_index=True)
    st.download_button("Download bus CSV", buses.to_csv(index=False), "bus_results.csv", "text/csv")
    st.download_button("Download line CSV", lines.to_csv(index=False), "line_results.csv", "text/csv")
    st.download_button("Download N-1 CSV", contingencies.to_csv(index=False), "n1_contingency_ranking.csv", "text/csv")
    st.subheader("Demand-growth sensitivity")
    scenarios = evaluate_load_growth(case, tuple(1 + x / 100 for x in range(0, 51, 10)))
    st.line_chart(scenarios.set_index("demand_growth_pct")[["max_line_loading_pct"]])
    st.dataframe(scenarios.round(2), use_container_width=True, hide_index=True)
except ValueError as exc:
    st.error(f"Cannot solve this scenario: {exc}")
    st.info("A line outage that disconnects the network makes the reduced linear system unsolvable.")
