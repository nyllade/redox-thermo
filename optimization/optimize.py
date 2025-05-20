# optimize.py — runs optimization and generates summary table + plots
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from main.thermodynamics import (
    calculate_Q,
    adjust_E0,
    calculate_deltaG,
    calculate_exergy_efficiency_from_H
)
from main.data import redox_pairs

# Output path
csv_path = os.path.join(os.path.dirname(__file__), "optimal_conditions.csv")

def optimize_environment_for_redox(pair, temp_range=(300, 373), pH_range=(5, 9), steps=20):
    best_result = None
    best_eff = -np.inf

    T_values = np.linspace(*temp_range, steps)
    pH_values = np.linspace(*pH_range, steps)

    for T in T_values:
        for pH in pH_values:
            if "H+" in pair["conc"]:
                pair["conc"]["H+"] = 10 ** (-pH)

            Q = calculate_Q(pair)
            E = adjust_E0(pair['E0'], pair['n'], T, Q)
            dG = calculate_deltaG(E, pair['n'])
            ex_eff = calculate_exergy_efficiency_from_H(dG, pair['delta_H'])

            if ex_eff > best_eff:
                best_eff = ex_eff
                best_result = {
                    "Redox Pair": pair['name'],
                    "T (K)": round(T, 2),
                    "pH": round(pH, 2),
                    "ΔG (kJ/mol)": round(dG / 1000, 2),
                    "Exergy Efficiency (%)": round(ex_eff, 2)
                }

    return best_result

def run_optimization_for_all():
    all_results = []
    for pair in redox_pairs:
        result = optimize_environment_for_redox(pair)
        all_results.append(result)
        print(f"Best conditions for: {result['Redox Pair']}")
        for k, v in result.items():
            if k != "Redox Pair":
                print(f"  {k}: {v}")
        print("-")

    df = pd.DataFrame(all_results)
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Optimization results saved to {csv_path}.")

if __name__ == "__main__":
    run_optimization_for_all()

    # Generate LaTeX table and plots
    import generate_optimal_table
    generate_optimal_table.generate_latex_table()

    import plot_optimal
    plot_optimal.generate_optimal_plots()