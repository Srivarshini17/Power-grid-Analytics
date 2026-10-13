from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def save_network_plot(buses: pd.DataFrame, lines: pd.DataFrame, path: Path):
    graph = nx.Graph()
    for row in lines.itertuples(index=False):
        graph.add_edge(int(row.from_bus), int(row.to_bus), label=row.line)
    pos = nx.spring_layout(graph, seed=42)
    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="#d8e9f8", edgecolors="#24527a", ax=ax)
    nx.draw_networkx_labels(graph, pos, ax=ax)
    nx.draw_networkx_edges(graph, pos, width=1.7, edge_color="#6b7280", ax=ax)
    labels = {(int(r.from_bus), int(r.to_bus)): r.line for r in lines.itertuples(index=False)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=8, ax=ax)
    ax.set_title("Synthetic transmission network topology")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def save_contingency_plot(contingencies: pd.DataFrame, path: Path):
    data = contingencies.replace([float("inf")], float("nan")).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data["outaged_line"], data["max_loading_pct"])
    ax.axhline(100, linestyle="--", linewidth=1.2, label="Thermal limit (100%)")
    ax.set_ylabel("Maximum remaining line loading (%)")
    ax.set_title("N-1 contingency severity (top-ranked outages)")
    ax.tick_params(axis="x", rotation=35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

def save_load_growth_plot(scenarios: pd.DataFrame, path: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(scenarios["demand_growth_pct"], scenarios["max_line_loading_pct"], marker="o", label="Maximum line loading")
    ax.axhline(100, linestyle="--", linewidth=1.2, label="Thermal limit (100%)")
    ax.set_xlabel("Demand growth (%)")
    ax.set_ylabel("Maximum line loading (%)")
    ax.set_title("Impact of demand growth on transmission loading")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
