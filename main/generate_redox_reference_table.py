# plot_redox_table.py
# Generates a LaTeX table of redox pair reference data
# including name, reaction, n, E0, and delta_H from main/data.py.

import os
import sys
# if this script lives in, say, main/scripts/, and your data.py is in main/,
# this will let you do `from data import redox_pairs`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import redox_pairs

def generate_redox_reference_table():
    output_path = "report/tables/table_redox_reference.tex"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write("\\begin{tabular}{l l c r r}\n")
        f.write("\\toprule\n")
        f.write("Redox Pair & Reaction & $n$ & $E^0$ (V) & $\\Delta H$ (kJ/mol) \\\\\n")
        f.write("\\midrule\n")

        for pair in redox_pairs:
            name     = pair.get("name", "N/A")
            reaction = pair.get("reaction", "N/A")
            n        = pair.get("n", "")
            E0       = pair.get("E0", "")
            delta_H  = pair.get("delta_H", "")

            # escape any underscores in LaTeX
            reaction = reaction.replace("_", "\\_")

            f.write(f"{name} & {reaction} & {n} & {E0} & {delta_H} \\\\\n")

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")

    print(f"Redox reference LaTeX table written to {output_path}")

if __name__ == "__main__":
    generate_redox_reference_table()