# plot_sensitivity.py
# Generates summary plots from sensitivity_summary.csv: scatter + fragility bar + concentration sensitivity

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from main.thermodynamics import calculate_Q, adjust_E0, calculate_deltaG
from main.data import redox_pairs

# Paths
summary_path = "sensitivity/sensitivity_summary.csv"
png_dir      = "sensitivity/figures_summary"
pdf_dir      = "report/figures"
os.makedirs(png_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

def plot_stability_scatter():
    df = pd.read_csv(summary_path)
    df["Directional Fragility"] = df["ΔG Range (T)"] - df["ΔG Range (pH)"]

    fig, ax = plt.subplots(figsize=(10, 7))
    palette = {"Stable": "#4CAF50", "Moderate": "#FFC107", "Sensitive": "#F44336"}
    df["Color"] = df["Stability"].map(palette).fillna("gray")

    label_positions = set()
    offset_templates = [(5, 5), (-5, 5), (5, -5), (-5, -5), (0, 8), (8, 0), (-8, 0), (0, -8)]
    offset_cycle = iter(offset_templates * (len(df) // len(offset_templates) + 1))

    for _, row in df.iterrows():
        x = row["ΔG Range (T)"]
        y = row["Exergy Range (T)"]
        size = 80 + 4 * abs(row["Directional Fragility"])
        color = row["Color"]
        label = row["Redox Pair"]
        ax.scatter(x, y, s=size, color=color, edgecolor="black", alpha=0.9)

        dx, dy = next(offset_cycle)
        ha = "left" if dx >= 0 else "right"
        va = "bottom" if dy >= 0 else "top"

        ax.annotate(
            label,
            xy=(x, y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8,
            ha=ha,
            va=va,
            bbox=dict(boxstyle="round,pad=0.2",
                      facecolor="white",
                      alpha=0.7,
                      edgecolor="none")
        )

    handles_color = [mpatches.Patch(color=c, label=l) for l, c in palette.items()]
    size_vals = [0, 30, 60, 90]
    size_handles = [
        Line2D([0], [0], marker='o', color='gray', label=f"{v:+} kJ/mol",
               markersize=np.sqrt(80 + 4 * abs(v)), linestyle='None')
        for v in size_vals
    ]

    legend1 = ax.legend(
        handles=handles_color,
        title="Stability",
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
        frameon=True,
        borderpad=0.5
    )
    ax.add_artist(legend1)

    legend2 = ax.legend(
        handles=size_handles,
        title="Fragility (ΔG_T − ΔG_pH)",
        loc="upper right",
        bbox_to_anchor=(0.82, 0.98),
        frameon=True,
        borderpad=0.5
    )

    ax.set_xlabel("ΔG Range across Temperature (kJ/mol)")
    ax.set_ylabel("Exergy Efficiency Range across Temperature (%)")
    ax.set_title("Stability & Fragility of Redox Pairs")
    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(png_dir, "stability_scatter_plot.png"), dpi=300)
    fig.savefig(os.path.join(pdf_dir, "stability_scatter_plot.pdf"))
    plt.close(fig)

def plot_directional_fragility():
    df = pd.read_csv(summary_path)
    df["Directional Fragility"] = df["ΔG Range (T)"] - df["ΔG Range (pH)"]
    df = df.sort_values("Directional Fragility", ascending=False)

    color_map = {"Stable": "#4CAF50", "Moderate": "#FFC107", "Sensitive": "#F44336"}
    bar_colors = df["Stability"].map(color_map).fillna("gray")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df["Redox Pair"], df["Directional Fragility"], color=bar_colors)

    for i, val in enumerate(df["Directional Fragility"]):
        x_text = val + (2 if val >= 0 else -3.5)
        ha = "left" if val >= 0 else "right"
        ax.text(x_text, i, f"{val:+.1f}", va="center", ha=ha, fontsize=8)

    ax.axvline(0, color="gray", linestyle="--")
    ax.set_xlim(-170, None)
    ax.set_xlabel("ΔG Range(T) − ΔG Range(pH) [kJ/mol]")
    ax.set_title("Directional Thermodynamic Fragility of Redox Pairs")

    stability_legend = [mpatches.Patch(color=c, label=l)
                        for l, c in color_map.items()]
    ax.legend(handles=stability_legend, title="Stability", loc="lower left")

    fig.tight_layout()
    fig.savefig(os.path.join(png_dir, "directional_fragility_bar.png"), dpi=300)
    fig.savefig(os.path.join(pdf_dir, "directional_fragility_bar.pdf"))
    plt.close(fig)
    print("✅ Final fragility bar chart saved.")

def plot_concentration_sensitivity():
    sweep_species = {
        "CO2/CH4": "CO2",
        "CO2/CO": "CO2",
        "NO3-/NO2-": "NO3-",
        "Fe3+/Fe2+": "Fe3+"
    }
    T = 300
    pH = 7
    concentrations = np.logspace(-8, -2, 100)

    plt.figure(figsize=(10, 6))
    for pair in redox_pairs:
        name = pair["name"]
        if name not in sweep_species:
            continue
        species = sweep_species[name]
        dG_vals = []

        for conc in concentrations:
            pair["conc"][species] = conc
            if "H+" in pair["conc"]:
                pair["conc"]["H+"] = 10 ** (-pH)
            Q = calculate_Q(pair)
            E = adjust_E0(pair["E0"], pair["n"], T, Q)
            dG = calculate_deltaG(E, pair["n"])
            dG_vals.append(dG / 1000)

        plt.plot(np.log10(concentrations), dG_vals, label=name)

    plt.xlabel("log₁₀ [Reactant] (M)")
    plt.ylabel("ΔG (kJ/mol)")
    plt.title("ΔG vs Reactant Concentration Sensitivity")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(png_dir, "concentration_sensitivity.png"), dpi=300)
    plt.savefig(os.path.join(pdf_dir, "concentration_sensitivity.pdf"))
    plt.close()
    print("✅ Concentration sensitivity plot saved.")

def generate_all_sensitivity_plots():
    plot_stability_scatter()
    plot_directional_fragility()
    plot_concentration_sensitivity()
    print("✅ All sensitivity plots saved to figures_summary/ and report/figures/")

if __name__ == "__main__":
    generate_all_sensitivity_plots()
















