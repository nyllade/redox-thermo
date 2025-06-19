# This script generates main simulation plots:
# - ΔG by redox pair and environment
# - Exergy efficiency by redox pair and environment
# - Redox ladder based on E⁰ and ΔH from reference data

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "results.csv")
figures_png = os.path.join(base_dir, "../main/figures_main")
figures_pdf = os.path.join(base_dir, "../report/figures")
os.makedirs(figures_png, exist_ok=True)
os.makedirs(figures_pdf, exist_ok=True)

def plot_dG_by_redox_and_env():
    df = pd.read_csv(csv_path)
    df["Redox Pair"] = df["Redox Pair"].astype(str)
    order = df.groupby("Redox Pair")["ΔG (kJ/mol)"].mean().sort_values().index

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df,
        x="Redox Pair",
        y="ΔG (kJ/mol)",
        hue="Environment",
        order=order,
        palette="crest"
    )
    plt.title("ΔG by Redox Pair and Environment")
    plt.ylabel("ΔG (kJ/mol)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_pdf, "deltaG_by_environment.pdf"))
    plt.savefig(os.path.join(figures_png, "deltaG_by_environment.png"), dpi=300)
    plt.close()

def plot_exergy_efficiency():
    df = pd.read_csv(csv_path)
    df["Redox Pair"] = df["Redox Pair"].astype(str)
    order = df.groupby("Redox Pair")["Exergy Eff (ΔH%)"].mean().sort_values(ascending=False).index

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df,
        x="Redox Pair",
        y="Exergy Eff (ΔH%)",
        hue="Environment",
        order=order,
        palette="mako"
    )
    plt.title("Exergy Efficiency (ΔH-based) by Redox Pair and Environment")
    plt.ylabel("Exergy Efficiency (%)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_pdf, "exergy_efficiency_H.pdf"))
    plt.savefig(os.path.join(figures_png, "exergy_efficiency_H.png"), dpi=300)
    plt.close()

def plot_redox_ladder():
    from data import redox_pairs
    ladder = []
    for pair in redox_pairs:
        name = pair.get("name")
        E0 = pair.get("E0")
        dH = pair.get("delta_H")
        n = pair.get("n")
        if None in (E0, dH, n):
            continue
        dG0 = -n * 96485 * E0 / 1000  # kJ/mol
        ex_eff = 100 * dG0 / dH if dH != 0 else 0
        ladder.append({
            "Redox Pair": name,
            "E0": E0,
            "Exergy Eff (%)": round(ex_eff, 2)
        })

    df = pd.DataFrame(ladder).sort_values(by="E0", ascending=False)

    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=df,
        x="E0",
        y="Redox Pair",
        hue="Redox Pair",
        palette="coolwarm"
    )
    plt.xlabel("Standard Redox Potential E$^0$ (V)")
    plt.title("Redox Ladder Colored by Exergy Efficiency")
    plt.legend([], [], frameon=False)  # Remove legend

    plt.tight_layout()
    plt.savefig(os.path.join(figures_pdf, "redox_ladder.pdf"))
    plt.savefig(os.path.join(figures_png, "redox_ladder.png"), dpi=300)
    plt.close()

def generate_all_plots():
    plot_dG_by_redox_and_env()
    plot_exergy_efficiency()
    plot_redox_ladder()
    print("✅ Main simulation plots saved to figures_main/ and report/figures/figures_main/")

if __name__ == "__main__":
    generate_all_plots()


