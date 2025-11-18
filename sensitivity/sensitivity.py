# sensitivity.py — runs simulations + summary + plotting

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Allow import of main/ modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main.thermodynamics import (
    calculate_Q,
    adjust_E0,
    calculate_deltaG,
    calculate_exergy_efficiency_from_H
)
from main.data import redox_pairs
import sensitivity_summary
from plot_sensitivity import generate_all_sensitivity_plots

# Paths
figures_path = "sensitivity/figures_sensitivity"
data_path = "sensitivity/data_sensitivity"
report_fig_path = "report/figures/figures_sensitivity"
os.makedirs(figures_path, exist_ok=True)
os.makedirs(data_path, exist_ok=True)
os.makedirs(report_fig_path, exist_ok=True)

def safe_filename(name):
    return name.replace("/", "_").replace("^", "").replace("+", "p").replace("-", "m")

def run_sensitivity_analysis():
    for pair in redox_pairs:
        print(f"▶ Running pH and T sensitivity sweeps for {pair['name']}...")
        safe_name = safe_filename(pair["name"])

        # === pH sweep at fixed T ===
        T_fixed = 300.0
        pH_range = np.linspace(4, 10, 50)
        dG_pH = []
        ex_pH = []

        for pH in pH_range:
            conc = pair["conc"].copy()
            if "H+" in conc:
                conc["H+"] = 10 ** (-pH)
            Q = calculate_Q({**pair, "conc": conc})
            E = adjust_E0(pair['E0'], pair['n'], T_fixed, Q)
            dG = calculate_deltaG(E, pair['n'])

            # Safe exergy efficiency
            ex_eff = np.nan if abs(pair['delta_H']) < 1e-8 else calculate_exergy_efficiency_from_H(dG, pair['delta_H'])

            dG_pH.append(dG / 1000)
            ex_pH.append(ex_eff)

        df_pH = pd.DataFrame({
            "pH": pH_range,
            "ΔG (kJ/mol)": dG_pH,
            "Exergy Efficiency (%)": ex_pH
        })
        df_pH.to_csv(f"{data_path}/{safe_name}_pH_sweep.csv", index=False)

        # Plot ΔG vs pH
        plt.figure()
        plt.plot(pH_range, dG_pH, label="ΔG (kJ/mol)", color="blue")
        plt.xlabel("pH")
        plt.ylabel("ΔG (kJ/mol)")
        plt.title(f"ΔG vs pH for {pair['name']}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{report_fig_path}/{safe_name}_dg_vs_pH.pdf")
        plt.savefig(f"{figures_path}/{safe_name}_dg_vs_pH.png", dpi=300)
        plt.close()

        # Plot Exergy vs pH
        if not np.all(np.isnan(ex_pH)):
            ex_pH_arr = np.array(ex_pH)
            valid_mask = ~np.isnan(ex_pH_arr)
            plt.figure()
            plt.plot(pH_range[valid_mask], ex_pH_arr[valid_mask], label="Exergy Efficiency (%)", color="green")
            plt.xlabel("pH")
            plt.ylabel("Exergy Efficiency (%)")
            plt.title(f"Exergy vs pH for {pair['name']}")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{report_fig_path}/{safe_name}_exergy_vs_pH.pdf")
            plt.savefig(f"{figures_path}/{safe_name}_exergy_vs_pH.png", dpi=300)
            plt.close()

        # === T sweep at fixed pH ===
        T_range = np.linspace(280, 400, 50)
        dG_T = []
        ex_T = []
        fixed_pH = 7.0
        conc = pair["conc"].copy()
        if "H+" in conc:
            conc["H+"] = 10 ** (-fixed_pH)

        for T in T_range:
            Q = calculate_Q({**pair, "conc": conc})
            E = adjust_E0(pair['E0'], pair['n'], T, Q)
            dG = calculate_deltaG(E, pair['n'])
            ex_eff = np.nan if abs(pair['delta_H']) < 1e-8 else calculate_exergy_efficiency_from_H(dG, pair['delta_H'])

            dG_T.append(dG / 1000)
            ex_T.append(ex_eff)

        df_T = pd.DataFrame({
            "T (K)": T_range,
            "ΔG (kJ/mol)": dG_T,
            "Exergy Efficiency (%)": ex_T
        })
        df_T.to_csv(f"{data_path}/{safe_name}_T_sweep.csv", index=False)

        # Plot ΔG vs T
        plt.figure()
        plt.plot(T_range, dG_T, label="ΔG (kJ/mol)", color="orange")
        plt.xlabel("Temperature (K)")
        plt.ylabel("ΔG (kJ/mol)")
        plt.title(f"ΔG vs Temperature for {pair['name']}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{report_fig_path}/{safe_name}_dg_vs_T.pdf")
        plt.savefig(f"{figures_path}/{safe_name}_dg_vs_T.png", dpi=300)
        plt.close()

        # Plot Exergy vs T
        if not np.all(np.isnan(ex_T)):
            ex_T_arr = np.array(ex_T)
            valid_mask_T = ~np.isnan(ex_T_arr)
            plt.figure()
            plt.plot(T_range[valid_mask_T], ex_T_arr[valid_mask_T], label="Exergy Efficiency (%)", color="purple")
            plt.xlabel("Temperature (K)")
            plt.ylabel("Exergy Efficiency (%)")
            plt.title(f"Exergy vs Temperature for {pair['name']}")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{report_fig_path}/{safe_name}_exergy_vs_T.pdf")
            plt.savefig(f"{figures_path}/{safe_name}_exergy_vs_T.png", dpi=300)
            plt.close()

    print("✅ Sensitivity sweeps complete. Data saved and plotted.")

if __name__ == "__main__":
    run_sensitivity_analysis()
    sensitivity_summary.generate_summary_table()
    generate_all_sensitivity_plots()