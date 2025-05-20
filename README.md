# 🧪 Thermodynamic Analysis of Prebiotic Redox Reactions

This project models and visualizes the thermodynamic feasibility of redox reactions relevant to the origin of life. It evaluates ΔG, exergy efficiency, environmental robustness, and optimal conditions across 12 redox pairs under varying pH and temperature.

---

## 📁 Project Structure
```
redox-thermo/
├── main/                     # Core simulation (ΔG, Exergy, Redox Ladder)
│   ├── main.py              # Simulates redox pairs across environments
│   ├── plotting.py          # Generates all main plots
│   ├── data.py              # Redox pair and environment definitions
│   ├── results.csv          # Simulation output
│   └── figures_main/        # Main plot outputs (.pdf and .png)
│
├── optimization/            # Optimal pH, T for max exergy
│   ├── optimize.py
│   ├── plot_optimal.py
│   └── figures_optimization/
│
├── sensitivity/             # Sensitivity to pH and T
│   ├── sensitivity.py
│   ├── plot_stability_bar.py
│   ├── plot_stability_scatter.py
│   ├── data_sensitivity/
│   ├── figures_sensitivity/
│   └── figures_summary/     # Summary figures (.pdf and .png)
│
├── report/
│   └── tables/              # Auto-generated LaTeX tables
│       ├── table_main_results.tex
│       ├── table_optimal_conditions.tex
│       ├── table_sensitivity_summary.tex
│       └── table_redox_reference.tex
```

---

## 📈 Features
- 🔬 Calculates ΔG and exergy efficiencies for redox reactions
- 🌍 Models reactions across acidic, alkaline, and neutral environments
- ⚙️ Finds optimal pH and T for highest exergy efficiency
- 📊 Analyzes sensitivity to environmental change
- 📄 Auto-generates LaTeX-ready figures and tables

---

## 🔧 Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Run the Full Pipeline
```bash
# Main simulations + plots + ladder + tables
python main/main.py

# Optimal condition discovery with visuals
python optimization/optimize.py

# Sensitivity sweeps + summary + visuals
python sensitivity/sensitivity.py
```

---

## 📚 Generated Outputs
- All figures saved in `/figures_.../` folders (PDF + PNG)
- All tables saved in `report/tables/`
- Ready to be included in Overleaf or other LaTeX systems

---

## 📜 License
MIT License

---

## 🤝 Credits
Developed by [Your Name], based on theoretical models and redox systems from origins-of-life research.

For academic use or collaboration, feel free to fork and cite.

---

## 🧠 Author
Developed by Eda Bağ, Genetics and Bioengineering Undergraduate, Spring 2025