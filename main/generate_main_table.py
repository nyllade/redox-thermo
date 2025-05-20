# This script reads simulation results from main/results.csv
# and creates a LaTeX table summarizing thermodynamic data
# for each redox pair in each environment.

import os
import pandas as pd

def generate_latex_table():
    csv_path = "main/results.csv"
    tex_path = "report/tables/table_main_results.tex"
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df.sort_values(by=["Environment", "Redox Pair"])

    with open(tex_path, "w") as f:
        f.write("\\begin{tabular}{l l r r r r}\n")
        f.write("\\toprule\n")
        f.write("Redox Pair & Environment & E (V) & $\\Delta G$ (kJ/mol) & ExG (\\%) & ExH (\\%) \\\\ \n")
        f.write("\\midrule\n")
        for _, row in df.iterrows():
            f.write(f"{row['Redox Pair']} & {row['Environment']} & {row['E (V)']} & {row['ΔG (kJ/mol)']} & {row['Exergy Eff (ΔG%)']} & {row['Exergy Eff (ΔH%)']} \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")

    print(f"LaTeX table written to {tex_path}")

if __name__ == "__main__":
    generate_latex_table()
