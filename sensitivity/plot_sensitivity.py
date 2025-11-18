import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from scipy.stats import linregress

from main.thermodynamics import calculate_Q, adjust_E0, calculate_deltaG
from main.data import redox_pairs

# Paths
summary_path = "sensitivity/sensitivity_summary.csv"
png_dir      = "sensitivity/figures_summary"
pdf_dir      = "report/figures/figures_sensitivity_summary"
os.makedirs(png_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

# Color palette for stability
PALETTE = {"Stable": "#4CAF50", "Moderate": "#FFC107", "Sensitive": "#F44336"}

def plot_stability_scatter():
    df = pd.read_csv(summary_path)
    df["Directional Fragility"] = df["ΔG Range (T)"].fillna(0) - df["ΔG Range (pH)"].fillna(0)
    df["Color"] = df["Stability"].map(PALETTE).fillna("gray")

    fig, ax = plt.subplots(figsize=(10, 7))

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
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor="white",
                      alpha=0.6,
                      linewidth=0)
        )

    handles_color = [mpatches.Patch(color=c, label=l) for l, c in PALETTE.items()]
    size_vals = [0, 30, 60, 90]
    size_handles = [
        Line2D([0], [0], marker='o', color='gray', label=f"{v:+} kJ/mol",
               markersize=np.sqrt(80 + 4 * abs(v)), linestyle='None')
        for v in size_vals
    ]

    legend1 = ax.legend(
        handles=handles_color,
        title="Stability",
        loc="center left",
        bbox_to_anchor=(1.02, 0.7),
        borderaxespad=0.,
        frameon=True
    )
    ax.add_artist(legend1)

    legend2 = ax.legend(
        handles=size_handles,
        title=r"Fragility ($\Delta G_T$ − $\Delta G_{pH}$)",
        loc="center left",
        bbox_to_anchor=(1.02, 0.3),
        borderaxespad=0.,
        frameon=True
    )

    ax.set_xlabel(r"$\Delta G$ Range across Temperature (kJ/mol)")
    ax.set_ylabel(r"Exergy Efficiency Range across Temperature (%)")
    ax.set_title("Stability & Fragility of Redox Pairs")
    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(png_dir, "stability_scatter_plot.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(pdf_dir, "stability_scatter_plot.pdf"), bbox_inches="tight")
    plt.close(fig)

def plot_directional_fragility():
    df = pd.read_csv(summary_path)
    df["Directional Fragility"] = df["ΔG Range (T)"].fillna(0) - df["ΔG Range (pH)"].fillna(0)
    df = df.sort_values("Directional Fragility", ascending=False)

    bar_colors = df["Stability"].map(PALETTE).fillna("gray")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df["Redox Pair"], df["Directional Fragility"], color=bar_colors)

    for i, val in enumerate(df["Directional Fragility"]):
        x_text = val + (2 if val >= 0 else -3.5)
        ha = "left" if val >= 0 else "right"
        ax.text(x_text, i, f"{val:+.1f}", va="center", ha=ha, fontsize=8)

    ax.axvline(0, color="gray", linestyle="--")
    xmin = min(df["Directional Fragility"].min(), 0) - 10
    xmax = max(df["Directional Fragility"].max(), 0) + 10
    ax.set_xlim(xmin, xmax)
    ax.set_xlabel(r"$\Delta G_{T}$ − $\Delta G_{pH}$ [kJ/mol]")
    ax.set_title("Directional Thermodynamic Fragility of Redox Pairs")

    stability_legend = [mpatches.Patch(color=c, label=l)
                        for l, c in PALETTE.items()]
    ax.legend(handles=stability_legend, title="Stability", loc="lower left")

    fig.tight_layout()
    fig.savefig(os.path.join(png_dir, "directional_fragility_bar.png"), dpi=300)
    fig.savefig(os.path.join(pdf_dir, "directional_fragility_bar.pdf"))
    plt.close(fig)
    print("✅ Final fragility bar chart saved.")

def plot_concentration_sensitivity():
    T = 300
    pH = 7
    concentrations = np.log10(np.logspace(-8, -2, 100))

    plt.figure(figsize=(10, 6))

    for pair in redox_pairs:
        name = pair["name"]
        reactants = list(pair.get("reactants", {}).keys())
        species = next((s for s in reactants if s != "H+"), reactants[0] if reactants else None)
        if species is None:
            continue

        dG_vals = []
        for conc_val in 10 ** concentrations:
            conc_copy = pair.get("conc", {}).copy()
            conc_copy[species] = conc_val
            if "H+" in conc_copy:
                conc_copy["H+"] = 10 ** (-pH)

            Q = calculate_Q({**pair, "conc": conc_copy})
            E = adjust_E0(pair["E0"], pair["n"], T, Q)
            dG = calculate_deltaG(E, pair["n"])
            dG_vals.append(dG / 1000)

        slope, _, _, _, _ = linregress(concentrations, dG_vals)
        label = f"{name} (slope: {slope:.2f})"
        plt.plot(concentrations, dG_vals, label=label)

    plt.xlabel(r"$\log_{10}$ [Reactant] (M)")
    plt.ylabel(r"$\Delta G$ (kJ/mol)")
    plt.title(r"$\Delta G$ vs Reactant Concentration Sensitivity")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=8)
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