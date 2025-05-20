# This script reads the optimal redox conditions from a CSV file
# and generates a LaTeX-formatted table for Overleaf integration.

import os
import pandas as pd

def generate_latex_table():
    csv_path = "optimization/optimal_conditions.csv"
    tex_path = "report/tables/table_optimal_conditions.tex"
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)

    df = pd.read_csv(csv_path)

    with open(tex_path, "w") as f:
        f.write("\\begin{tabular}{lccc}\n")
        f.write("\\toprule\n")
        f.write("Redox Pair & Temperature (K) & pH & Exergy Efficiency (\\%) \\\\ \n")
        f.write("\\midrule\n")
        for _, row in df.iterrows():
            f.write(f"{row['Redox Pair']} & {row['T (K)']} & {row['pH']} & {row['Exergy Efficiency (%)']} \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")

    print(f"LaTeX table written to {tex_path}")

if __name__ == "__main__":
    generate_latex_table()
