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
    df["Exergy Efficiency (%)"] = pd.to_numeric(df["Exergy Efficiency (%)"], errors="coerce")
    df = df.dropna(subset=["Exergy Efficiency (%)"])

    # Clip extreme values for visual clarity
    df["Clipped Exergy (%)"] = df["Exergy Efficiency (%)"].clip(-300, 300)
    df["Clipped?"] = df["Clipped Exergy (%)"] != df["Exergy Efficiency (%)"]

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(
        data=df,
        x="Redox Pair",
        y="Clipped Exergy (%)",
        hue="Redox Pair",
        palette="viridis"
    )

    # Add asterisk for clipped bars
    for i, row in df.iterrows():
        if row["Clipped?"]:
            y = row["Clipped Exergy (%)"]
            barplot.annotate("*", (i, y), textcoords="offset points", xytext=(0, 3),
                             ha='center', fontsize=10, color="red")

    plt.title("Optimal Exergy Efficiency by Redox Pair")
    plt.ylabel("Efficiency (%)")
    plt.xticks(rotation=45, ha='right')
    plt.legend().remove()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.figtext(0.99, 0.01,
                "*Values clipped to ±300% for clarity\nSome redox pairs excluded due to undefined exergy efficiency",
                ha="right", fontsize=8, style="italic")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir_pdf, "optimal_exergy_efficiency.pdf"))
    plt.savefig(os.path.join(fig_dir_png, "optimal_exergy_efficiency.png"), dpi=300)
    plt.close()

def plot_optimal_conditions_scatter():
    df = pd.read_csv(csv_path)

    df["Exergy Efficiency (%)"] = pd.to_numeric(df["Exergy Efficiency (%)"], errors="coerce")
    df["pH"] = pd.to_numeric(df["pH"], errors="coerce")
    df["T (K)"] = pd.to_numeric(df["T (K)"], errors="coerce")
    df = df.dropna(subset=["Exergy Efficiency (%)", "pH", "T (K)"])

    if df.empty:
        print("⚠️ No valid data to plot in optimal_conditions_scatter. Skipping.")
        return

    df["Clipped Eff (%)"] = df["Exergy Efficiency (%)"].clip(-100, 100)
    df["Point Size"] = 80 + 0.8 * (df["Clipped Eff (%)"] + 100)

    jittered_pH = df["pH"] + np.random.normal(0, 0.12, size=len(df))
    jittered_T = df["T (K)"] + np.random.normal(0, 1.2, size=len(df))

    df["Jittered pH"] = jittered_pH
    df["Jittered T"] = jittered_T
    df_sorted = df.sort_values("Point Size", ascending=False).reset_index(drop=True)

    plt.figure(figsize=(10, 6))
    colors = sns.color_palette("Set2", n_colors=len(df_sorted))

    for i, row in df_sorted.iterrows():
        plt.scatter(row["Jittered pH"], row["Jittered T"],
                    s=row["Point Size"],
                    color=colors[i],
                    edgecolor="black",
                    label=f"{row['Redox Pair']} ({row['Clipped Eff (%)']:+.0f}%)")

    plt.xlabel("pH")
    plt.ylabel("Temperature (K)")
    plt.title("Optimal pH and Temperature by Redox Pair")
    plt.xlim(4, 10)
    plt.ylim(280, 400)
    plt.grid(True, linestyle="--", alpha=0.5)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(),
               loc="upper center",
               bbox_to_anchor=(0.5, -0.15),
               ncol=3, fontsize=8, title="Redox Pair – Exergy Efficiency")

    plt.figtext(0.99, 0.01,
                "*Some redox pairs excluded due to undefined exergy efficiency",
                ha="right", fontsize=8, style="italic")

    plt.tight_layout(rect=[0, 0.05, 1, 1])
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
    plt.legend().remove()
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