from pathlib import Path
from grid_analysis.sample_network import make_sample_case
from grid_analysis.solver import solve_power_flow
from grid_analysis.contingency import run_n1_analysis
from grid_analysis.scenarios import evaluate_load_growth
from grid_analysis.reporting import save_network_plot, save_contingency_plot, save_load_growth_plot

def main():
    root = Path(__file__).resolve().parent
    output = root / "results"
    output.mkdir(exist_ok=True)
    case = make_sample_case()
    buses, lines, diag = solve_power_flow(case)
    contingencies = run_n1_analysis(case)
    scenarios = evaluate_load_growth(case)

    buses.to_csv(output / "base_case_bus_results.csv", index=False)
    lines.to_csv(output / "base_case_line_results.csv", index=False)
    contingencies.to_csv(output / "n1_contingency_ranking.csv", index=False)
    scenarios.to_csv(output / "load_growth_scenarios.csv", index=False)
    save_network_plot(case.buses, case.lines, output / "base_case_network.png")
    save_contingency_plot(contingencies, output / "contingency_ranking.png")
    save_load_growth_plot(scenarios, output / "load_growth.png")

    print("=" * 60)
    print("POWER GRID ANALYTICS & CONTINGENCY PLANNING")
    print("=" * 60)
    print(f"Network: {case.name} | Buses: {len(case.buses)} | Lines: {len(case.lines)}")
    print(f"Demand: {diag['total_load_mw']:.2f} MW")
    print(f"Slack balancing injection: {diag['slack_injection_mw']:.2f} MW")
    print(f"Power balance error: {diag['power_balance_error_mw']:.3e} MW")
    print(f"Reduced matrix condition number: {diag['matrix_condition_number']:.3f}")
    print("\nBase-case line loadings:")
    print(lines[["line", "flow_mw", "limit_mw", "loading_pct", "overloaded"]].round(2).to_string(index=False))
    print("\nTop N-1 contingencies:")
    print(contingencies.head(5).round(2).to_string(index=False))
    print("\nDemand-growth scenarios:")
    print(scenarios.round(2).to_string(index=False))
    print(f"\nCSV reports and plots saved in: {output}")
    print("Analysis completed.")

if __name__ == "__main__":
    main()
