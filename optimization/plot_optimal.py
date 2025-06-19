# This script generates plots for the optimal conditions of redox pairs
# based on the results from the optimization process.
# It includes bar plots of exergy efficiency and ΔG, and a scatter plot of optimal conditions.
# The figures are saved to both optimization/figures_optimization and report/figures/figures_optimization.
# plot_optimal.py
# Generates bar and scatter plots for optimal redox conditions

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Paths
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "optimal_conditions.csv")
fig_dir_png = os.path.join(base_dir, "figures_optimization")
fig_dir_pdf = os.path.abspath(os.path.join(base_dir, "../report/figures/figures_optimization"))
os.makedirs(fig_dir_png, exist_ok=True)
os.makedirs(fig_dir_pdf, exist_ok=True)

def plot_optimal_exergy_efficiency():
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x="Redox Pair",
        y="Exergy Efficiency (%)",
        hue="Redox Pair",
        palette="viridis"
    )
    plt.title("Optimal Exergy Efficiency by Redox Pair")
    plt.ylabel("Efficiency (%)")
    plt.xticks(rotation=45, ha='right')
    plt.legend().remove()  # Manually remove legend
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir_pdf, "optimal_exergy_efficiency.pdf"))
    plt.savefig(os.path.join(fig_dir_png, "optimal_exergy_efficiency.png"), dpi=300)
    plt.close()

def plot_optimal_conditions_scatter():
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(8, 6))
    jittered_pH = df["pH"] + np.random.uniform(-0.25, 0.25, size=len(df))
    jittered_T = df["T (K)"] + np.random.uniform(-1.5, 1.5, size=len(df))
    colors = sns.color_palette("tab20", n_colors=len(df))

    for i in range(len(df)):
        size = 50 + (df["Exergy Efficiency (%)"][i] + 100) * 0.8
        eff_value = df["Exergy Efficiency (%)"][i]
        eff_str = f"{eff_value:+.0f}%"
        label = f"{df['Redox Pair'][i]} ({eff_str})"
        plt.scatter(jittered_pH[i], jittered_T[i], s=size, color=colors[i], label=label)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper right", title="Redox Pair – Exergy Efficiency")
    plt.title("Optimal pH and Temperature by Redox Pair")
    plt.xlabel("pH")
    plt.ylabel("Temperature (K)")
    plt.xlim(4, 10)
    plt.ylim(280, 400)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir_pdf, "optimal_conditions_scatter.pdf"))
    plt.savefig(os.path.join(fig_dir_png, "optimal_conditions_scatter.png"), dpi=300)
    plt.close()

def plot_optimal_dG():
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x="Redox Pair",
        y="ΔG (kJ/mol)",
        hue="Redox Pair",
        palette="magma"
    )
    plt.title("ΔG at Optimal Conditions by Redox Pair")
    plt.ylabel("ΔG (kJ/mol)")
    plt.xticks(rotation=45, ha='right')
    plt.legend().remove()  # Remove legend manually
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir_pdf, "optimal_dG.pdf"))
    plt.savefig(os.path.join(fig_dir_png, "optimal_dG.png"), dpi=300)
    plt.close()

def generate_optimal_plots():
    plot_optimal_exergy_efficiency()
    plot_optimal_conditions_scatter()
    plot_optimal_dG()
    print("✅ Optimization plots saved to both figures_optimization/ and report/figures/figures_optimization/.")

if __name__ == "__main__":
    generate_optimal_plots()