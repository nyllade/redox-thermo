import os
import pandas as pd

# Paths
data_dir = "sensitivity/data_sensitivity"
summary_csv = "sensitivity/sensitivity_summary.csv"
summary_tex = "report/tables/table_sensitivity_summary.tex"
os.makedirs(os.path.dirname(summary_tex), exist_ok=True)

# Stability classification thresholds
DG_THRESHOLDS = (10, 50)  # kJ/mol
EX_THRESHOLDS = (10, 50)  # %

def classify_stability(dg_range, ex_range):
    if dg_range < DG_THRESHOLDS[0] and ex_range < EX_THRESHOLDS[0]:
        return "Stable"
    elif dg_range < DG_THRESHOLDS[1] and ex_range < EX_THRESHOLDS[1]:
        return "Moderate"
    else:
        return "Sensitive"

def generate_summary_table():
    records = []

    for filename in os.listdir(data_dir):
        if not filename.endswith("_pH_sweep.csv"):
            continue

        base = filename.replace("_pH_sweep.csv", "")
        redox_label = base.replace("_", "/").replace("p", "+").replace("m", "-")

        df_pH = pd.read_csv(os.path.join(data_dir, filename))
        df_T = pd.read_csv(os.path.join(data_dir, base + "_T_sweep.csv"))

        dg_range_pH = df_pH["ΔG (kJ/mol)"].max() - df_pH["ΔG (kJ/mol)"].min()
        dg_range_T  = df_T["ΔG (kJ/mol)"].max() - df_T["ΔG (kJ/mol)"].min()
        ex_range_pH = df_pH["Exergy Efficiency (%)"].max() - df_pH["Exergy Efficiency (%)"].min()
        ex_range_T  = df_T["Exergy Efficiency (%)"].max() - df_T["Exergy Efficiency (%)"].min()

        stability = classify_stability(max(dg_range_pH, dg_range_T), max(ex_range_pH, ex_range_T))

        records.append({
            "Redox Pair": redox_label,
            "ΔG Range (pH)": round(dg_range_pH, 2),
            "ΔG Range (T)": round(dg_range_T, 2),
            "Exergy Range (pH)": round(ex_range_pH, 2),
            "Exergy Range (T)": round(ex_range_T, 2),
            "Stability": stability
        })

    # Save CSV
    summary_df = pd.DataFrame(records)
    summary_df.to_csv(summary_csv, index=False)

    # Save LaTeX table
    with open(summary_tex, "w") as f:
        f.write("\\begin{tabular}{lccccc}\n")
        f.write("\\toprule\n")
        f.write("Redox Pair & $\\Delta G_{pH}$ & $\\Delta G_T$ & Exergy$_{pH}$ & Exergy$_T$ & Stability \\\\ \n")
        f.write("\\midrule\n")
        for row in records:
            f.write(f"{row['Redox Pair']} & {row['ΔG Range (pH)']} & {row['ΔG Range (T)']} & "
                    f"{row['Exergy Range (pH)']}\% & {row['Exergy Range (T)']}\% & {row['Stability']} \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")

    print(f"Summary table saved to {summary_csv} and {summary_tex}")
