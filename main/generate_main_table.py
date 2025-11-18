import os
import pandas as pd

def tex_escape(s):
    return str(s).replace("_", "\\_")

def format_redox_pair(name):
    return {
        "CO2/CH3COO-": r"CO$_2$/CH$_3$COO$^-$",
        "CO2/CH4": r"CO$_2$/CH$_4$",
        "Fe3+/Fe2+": r"Fe$^{3+}$/Fe$^{2+}$",
        "H2/H+": r"H$_2$/H$^+$",
        "NO3-/NO2-": r"NO$_3^-$/NO$_2^-$",
        "SO42-/H2S": r"SO$_4^{2-}$/H$_2$S"
    }.get(name, tex_escape(name))

def format_environment(env):
    return {
        "acidicocean": r"\textit{acidic ocean}",
        "alkalinevent": r"\textit{alkaline vent}",
        "shallowpond": r"\textit{shallow pond}"
    }.get(env, tex_escape(env))

def generate_latex_table():
    csv_path = "main/results.csv"
    tex_path = "report/tables/table_main_results.tex"
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df.sort_values(by=["Environment", "Redox Pair"])

    with open(tex_path, "w") as f:
        f.write(r"""\begin{tabular}{l l S[table-format=-1.3] S[table-format=-4.2] S[table-format=-4.0] S[table-format=-4.0]}
\toprule
Redox Pair & Environment & {E (V)} & {$\Delta G$ (kJ/mol)} & {ExG (\%)} & {ExH (\%)} \\
\midrule
""")
        for _, row in df.iterrows():
            f.write(
                f"{format_redox_pair(row['Redox Pair'])} & "
                f"{format_environment(row['Environment'])} & "
                f"{row['E (V)']:.3f} & "
                f"{row['ΔG (kJ/mol)']:.2f} & "
                f"{row['Exergy Eff (ΔG%)']:.0f} & "
                f"{row['Exergy Eff (ΔH%)']:.0f} \\\\ \n"
            )

        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")

    print(f"✅ LaTeX table written to {tex_path}")

if __name__ == "__main__":
    generate_latex_table()