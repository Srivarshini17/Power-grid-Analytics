# Project Report: Power Grid Analytics & Contingency Planning

## Abstract
This project uses linear algebra to analyze a simplified transmission network. It solves a DC power-flow model, calculates branch active-power flows, screens single-line outages, and studies demand-growth sensitivity.

## Objectives
1. Represent buses and lines as structured tables.
2. Build and solve the reduced bus-susceptance matrix.
3. Calculate line flow and thermal loading.
4. Rank N-1 line outages by severity.
5. Study how demand growth affects line loading.

## Method
For each branch `(i, j)`, the DC approximation uses `P_ij = (theta_i - theta_j) / x_ij`. The bus-susceptance matrix is assembled from inverse reactances. The slack-bus angle is fixed to zero; the reduced system is solved using NumPy. The slack injection balances net injections at the remaining buses.

## Results to complete
Run `python main.py`. Use the generated CSV files to discuss:
- The most heavily loaded lines in the base case.
- Which outages cause the largest overloads.
- How increasing demand changes maximum line loading.
- Numerical power-balance error and matrix condition number.

## Limitations
The model ignores reactive power, voltage-magnitude changes, resistive losses, generator constraints, and dynamic stability. The network is synthetic and intended for learning, not operational decisions.

## Future work
- Add a properly cited public benchmark dataset.
- Compare with a validated AC power-flow implementation.
- Add generation dispatch optimization and uncertain-load scenarios.
