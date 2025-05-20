# This script simulates redox reactions across different environments.
# It calculates ΔG and exergy efficiencies for each redox pair in each environment,
# and exports the results and summary plots.

import os

base_dir = os.path.dirname(__file__)
figures_path = os.path.join(base_dir, "figures_main")
results_path = os.path.join(base_dir, "results.csv")
os.makedirs(figures_path, exist_ok=True) # Ensure figures folder exists

import pandas as pd # for data manipulation

from thermodynamics import ( 
    # for thermodynamic calculations
    calculate_Q,
    adjust_E0,
    calculate_deltaG,
    calculate_exergy_efficiency_from_G,
    calculate_exergy_efficiency_from_H
)

from data import redox_pairs, environments # for redox pairs and environmental conditions

def run_simulation():
    results = []
    for env in environments:
        for pair in redox_pairs:
            # Update [H+] based on pH
            if "H+" in pair["conc"]:
                pair["conc"]["H+"] = 10 ** (-env["pH"])

            Q = calculate_Q(pair)
            E_adj = adjust_E0(pair['E0'], pair['n'], env['T'], Q)
            dG = calculate_deltaG(E_adj, pair['n'])
            dG0 = calculate_deltaG(pair['E0'], pair['n'])

            ex_eff_G = calculate_exergy_efficiency_from_G(dG, dG0)
            ex_eff_H = calculate_exergy_efficiency_from_H(dG, pair['delta_H'])

            results.append({
                "Redox Pair": pair['name'],
                "Reaction": pair['reaction'],
                "Environment": env['name'],
                "E (V)": round(E_adj, 4),
                "ΔG (kJ/mol)": round(dG / 1000, 2),
                "Exergy Eff (ΔG%)": round(ex_eff_G, 2),
                "Exergy Eff (ΔH%)": round(ex_eff_H, 2)
            })
    return results

def export_results(results, filename="results.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"\nResults exported to {filename}")

def print_results(results):
    print("\nThermodynamic Simulation Results:")
    for r in results:
        print(f"{r['Redox Pair']} in {r['Environment']} → E: {r['E (V)']} V, ΔG: {r['ΔG (kJ/mol)']} kJ/mol, ExG: {r['Exergy Eff (ΔG%)']}%, ExH: {r['Exergy Eff (ΔH%)']}%")

if __name__ == "__main__":
    results = run_simulation()
    print_results(results)
    export_results(results, filename=results_path)

    from plotting import generate_all_plots
    generate_all_plots()

    # Auto-generate tables and redox ladder figure
    import generate_main_table
    generate_main_table.generate_latex_table()

    import generate_redox_reference_table
    generate_redox_reference_table.generate_redox_reference_table()
