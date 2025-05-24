# Thermodynamic Analysis of Redox Reactions

This project performs a theoretical thermodynamic analysis of key redox reactions that are relevant to early Earth environments and the origin of life. It models standard Gibbs free energy (ΔG), exergy efficiency (both ΔG- and ΔH-based), and identifies optimal reaction conditions under varying pH and temperature. Additionally, it assesses the sensitivity of each redox pair to environmental changes and generates reproducible visualizations and LaTeX-compatible summary tables.

---

## 🔬 Scientific Objective

This study explores how specific redox reactions may have behaved across plausible prebiotic conditions. We aim to:

- Quantify reaction favorability (ΔG) and efficiency (exergy) across environments
- Identify optimal pH and temperature conditions for each reaction
- Assess how ΔG and exergy vary with pH, temperature, and concentration
- Provide high-quality output for integration into a scientific report or paper

---

## 🗂️ Project Structure

```
redox-thermo/
├── main/                                 # Baseline thermodynamic simulations across 3 early Earth environments
│   ├── main.py                           # Runs all simulations and generates outputs
│   ├── plotting.py                       # High-quality visualizations (ΔG, Exergy, Redox Ladder)
│   ├── generate_main_table.py            # Exports LaTeX table of ΔG, E, exergy per reaction & environment
│   ├── generate_redox_reference_table.py # Generates LaTeX table with reference E⁰ and ΔH values
│   ├── data.py                           # Defines redox pairs and environmental settings
│   ├── thermodynamics.py                 # Core thermodynamic calculations (Q, ΔG, efficiency)
│   ├── results.csv                       # Main simulation output data (ΔG, Exergy, etc.)
│   └── figures_main/                     # PNG previews of main result figures
│
├── optimization/                         # Optimal conditions (pH, T) per redox pair
│   ├── optimize.py                       # Finds conditions for max exergy efficiency
│   ├── plot_optimal.py                   # Plots: ΔG, exergy, and pH/T scatter under optimal conditions
│   ├── generate_optimal_table.py         # LaTeX summary table for optimal results
│   ├── optimal_conditions.csv            # Output data: best conditions per redox pair
│   └── figures_optimization/             # PNG previews of optimization result figures
│
├── sensitivity/                          # Sensitivity analysis (ΔG, exergy) to pH, temperature, concentration
│   ├── sensitivity.py                    # Runs sensitivity sweeps (pH, T, [CO₂]) and creates datasets
│   ├── plot_sensitivity.py               # Generates final summary plots (scatter, bar, concentration)
│   ├── sensitivity_summary.py            # Builds summary CSV and LaTeX table from 48 sweep datasets
│   ├── sensitivity_summary.csv           # Final summary table of sensitivity ranges
│   ├── data_sensitivity/                 # Raw sweep data (CSV files, per redox pair × axis)
│   ├── figures_sensitivity/              # Detailed sweep figures (PDF or PNG, 48 total)
│   └── figures_summary/                  # Final summary plots (PNG previews)
│
├── report/
│   ├── figures/                          # Publication-quality PDF figures from all modules
│   │   ├── figures_main/
│   │   ├── figures_optimization/
│   │   └── figures_sensitivity/
│   └── tables/                           # All LaTeX-formatted tables (for Overleaf or journal submission)
│
├── requirements.txt                      # Python dependencies (minimal list)
└── README.md                             # This file
```

---

## ⚙️ How to Run the Project

Each part of the pipeline can be executed independently:

### 1. 🔄 Simulate All Reactions (Main)
```bash
python main/main.py
```
- Computes ΔG, E, and exergy efficiency (ΔG & ΔH) for 12 redox pairs × 3 environments
- Outputs:
  - `main/results.csv`
  - 3 figures (ΔG, exergy, redox ladder)
  - 2 LaTeX tables

### 2. 📈 Optimize for Best Efficiency
```bash
python optimization/optimize.py
```
- Identifies best (pH, T) for max exergy efficiency for each redox pair
- Outputs:
  - `optimization/optimal_conditions.csv`
  - 3 figures (ΔG, exergy, scatter of pH vs T)
  - 1 LaTeX table

### 3. 🔬 Sensitivity Analysis
```bash
python sensitivity/sensitivity.py
```
- Sweeps pH, T, and [CO₂] for each reaction
- Summarizes how ΔG and exergy vary across conditions
- Outputs:
  - 48 sensitivity datasets
  - 3 summary plots (scatter, fragility, concentration)
  - 1 LaTeX table

---

## 🧾 Output Summary

This project generates a complete set of **publication-ready outputs** across all modules.  
It includes structured data files (CSV), scientific figures in both preview (PNG) and high-resolution (PDF) formats, and LaTeX tables ready for Overleaf or manuscript submission.

| **Type**                  | **File(s) / Folder**                                                                 | **Description**                                                                |
|---------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **CSV Results**           | `main/results.csv`                                                                  | Thermodynamic results for 12 redox pairs across 3 environments                |
|                           | `optimization/optimal_conditions.csv`                                               | Optimal pH and temperature with corresponding ΔG and exergy values            |
|                           | `sensitivity/sensitivity_summary.csv`                                               | Summary of ΔG and exergy sensitivity to temperature and pH                   |
|                           | `sensitivity/data_sensitivity/*.csv`                                                | Raw sweep data for 12 redox pairs × 2 axes (48 files total)                  |
|                           | `sensitivity/concentration_sensitivity.csv`                                         | Output from concentration sensitivity analysis                               |
| **LaTeX Tables**          | `report/tables/table_main_results.tex`                                              | ΔG, E, exergy efficiency per environment and redox pair                      |
|                           | `report/tables/table_redox_reference.tex`                                           | Redox reactions with E⁰, electron count (n), and ΔH                         |
|                           | `report/tables/table_optimal_conditions.tex`                                        | Best environmental conditions (pH, T) for each redox pair                   |
|                           | `report/tables/table_sensitivity_summary.tex`                                       | Categorized sensitivity levels (Stable, Moderate, Sensitive)                |
|                           | `report/tables/table_dG_env.tex`, `table_exergy_env.tex`                            | Environment-sorted ΔG and exergy tables                                     |
| **PNG Figures (Preview)** | `main/figures_main/`, `optimization/figures_optimization/`, `sensitivity/figures_summary/` | Quick-look preview figures for visual inspection                            |
| **Sweep Figures (48)**    | `sensitivity/figures_sensitivity/`                                                  | All T/pH sweep plots (ΔG vs T, ΔG vs pH, Exergy vs T, Exergy vs pH × 12)    |
| **PDF Figures (Final)**   | `report/figures/figures_main/`                                                      | High-resolution ΔG by environment, Exergy by environment, Redox ladder       |
|                           | `report/figures/figures_optimization/`                                              | Bar and scatter plots from optimization results                             |
|                           | `report/figures/figures_sensitivity/`                                               | Final stability, fragility, and concentration sensitivity plots              |

---

✅ All outputs are **automatically generated** upon script execution.  
✅ Figures are styled for use in scientific posters, conference presentations, and journal publications.

---

## 📦 Requirements

You can install all dependencies via:
```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
pandas
numpy
matplotlib
seaborn
jinja2
```

---

## 👩‍🔬 Author & Purpose

Developed by Eda Bağ, Genetics and Bioengineering Undergraduate, Spring 2025

This project was created as part of a research initiative on prebiotic chemistry and the thermodynamic feasibility of early redox systems. The scripts are designed to support publication-ready figures and results.

If you use this workflow or adapt it for your study, please cite accordingly.

Parts of this codebase (structure, plotting scripts, LaTeX generation, optimization routines, etc.) were developed with the assistance of AI tools, including ChatGPT. Human validation and customization ensured scientific accuracy and reproducibility.

---

## 📬 Feedback & Contributions
Questions, ideas, or improvements? Feel free to open an issue or fork the repo!
