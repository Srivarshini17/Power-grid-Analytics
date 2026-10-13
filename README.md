# Power Grid Analytics & Contingency Planning

A portfolio project using Python and linear algebra to analyze a **synthetic transmission network** with a DC power-flow approximation. It calculates bus voltage angles and line power flows, screens single-line outages (N-1 contingency analysis), tests demand-growth scenarios, exports reports, and provides an interactive Streamlit dashboard.

## Features
- Assemble and solve a reduced bus-susceptance matrix with NumPy.
- Calculate bus angles, line active-power flows, thermal loading, and overloads.
- Automatically balance scheduled injections at the slack bus.
- Screen every single-line outage and rank cases by severity.
- Compare demand growth from 0% to 50%.
- Export CSV reports and PNG plots.
- Interactive Streamlit dashboard with outage and demand controls.
- Six automated tests for power balance, flow equations, contingencies, scenarios, and input validation.

## Project structure
```text
power_grid_analytics_pro/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── REPORT.md
├── grid_analysis/
│   ├── __init__.py
│   ├── model.py
│   ├── sample_network.py
│   ├── solver.py
│   ├── contingency.py
│   ├── scenarios.py
│   └── reporting.py
├── tests/test_grid_analysis.py
├── data/README.md
└── results/
```

## Setup (Windows / VS Code)
Open a terminal in this folder:
```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```
If `(.venv)` is already visible, skip the first two commands.

## Run command-line analysis
```bat
python main.py
```
Generated files appear in `results/`:
- `base_case_bus_results.csv`
- `base_case_line_results.csv`
- `n1_contingency_ranking.csv`
- `load_growth_scenarios.csv`
- `base_case_network.png`
- `contingency_ranking.png`
- `load_growth.png`

## Launch dashboard
```bat
streamlit run app.py
```
Open the local URL printed in the terminal, usually `http://localhost:8501`.

## Run tests
```bat
python -m pytest -v
```

## Model summary
For a line from bus *i* to bus *j*, the DC approximation is:

`P_ij = (theta_i - theta_j) / x_ij`

where `x_ij` is per-unit line reactance and `theta` is the voltage angle in radians. The program builds the bus-susceptance matrix, fixes the slack-bus angle to zero, and solves the reduced linear system. The slack injection balances net injections at other buses.

## Resume description
**Power Grid Analytics & Contingency Planning | Python, NumPy, Pandas, NetworkX, Matplotlib, Streamlit, pytest**
- Built a DC power-flow solver by assembling and solving a reduced bus-susceptance matrix to calculate bus angles and transmission-line active-power flows.
- Automated N-1 transmission-line outage screening and ranked contingencies by line thermal-overload severity.
- Evaluated demand-growth scenarios, exported reproducible CSV reports and visualizations, and developed an interactive Streamlit dashboard.
- Added automated tests for power balance, line-flow equations, contingency coverage, and input validation.

Only list features you have run and can explain in an interview.

## Important limitations
This is a teaching/portfolio model with synthetic data, not an operational grid-planning tool. It approximates active-power flow and does not model reactive power, voltage magnitudes, line losses, generator limits, or dynamic stability. The included network is synthetic, not an official IEEE benchmark.
