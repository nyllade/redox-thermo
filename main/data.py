# This script generates plots for the optimal conditions of redox pairs based on the results from the optimization process.
# It includes functions to plot optimal exergy efficiency, scatter plots of optimal conditions, and bar plots of ΔG at optimal conditions.
# It also ensures that the figures directory exists before saving the plots.

# Redox pairs (12 total) with standard potentials, stoichiometry, concentrations, and ΔH
redox_pairs = [
    {
        "name": "H2/H+",
        "reaction": "2H+ + 2e- → H2",
        "E0": 0.000,  # Standard hydrogen electrode potential in V
        "n": 2,
        "delta_H": 0.000,  # kJ/mol
        "reactants": {"H+": 2},
        "products": {"H2": 1},
        "conc": {"H+": 1e-7, "H2": 1e-6}
    },
    {
        "name": "CO2/CH4",
        "reaction": "CO2 + 8H+ + 8e- → CH4 + 2H2O",
        "E0": -0.244,
        "n": 8,
        "delta_H": -44.5,  # kJ/mol (approx. combustion of CH4)
        "reactants": {"CO2": 1, "H+": 8},
        "products": {"CH4": 1},
        "conc": {"CO2": 1e-3, "CH4": 1e-6, "H+": 1e-7}
    },
    {
        "name": "NO3-/NO2-",
        "reaction": "NO3⁻ + 2H⁺ + 2e⁻ → NO2⁻ + H2O",
        "E0": 0.421,
        "n": 2,
        "delta_H": -90.53,  # estimated
        "reactants": {"NO3-": 1, "H+": 2},
        "products": {"NO2-": 1},
        "conc": {"NO3-": 1e-4, "NO2-": 1e-6, "H+": 1e-7}
    },
    {
        "name": "SO4^2-/H2S",
        "reaction": "SO₄²⁻ + 10H⁺ + 8e⁻ → H₂S + 4H₂O",
        "E0": -0.220,
        "n": 8,
        "delta_H": 105.87,  # Approximate enthalpy for sulfate reduction
        "reactants": {"SO4^2-": 1, "H+": 10},
        "products": {"H2S": 1, "H2O": 4},
        "conc": {"SO4^2-": 1e-3, "H2S": 1e-6, "H+": 1e-7}
    },
    {
        "name": "Fe3+/Fe2+",
        "reaction": "Fe³⁺ + e⁻ → Fe²⁺",
        "E0": 0.770,  # Standard redox potential in V vs SHE
        "n": 1,
        "delta_H": -40.2,  # Approximate ΔH in kJ/mol, literature varies from -18 to -20
        "reactants": {"Fe3+": 1},
        "products": {"Fe2+": 1},
        "conc": {"Fe3+": 1e-6, "Fe2+": 1e-6}
    },
    {
        "name": "CO2/CH3COO-",
        "reaction": "2CO₂ + 8H⁺ + 8e⁻ → CH₃COO⁻ + 2H₂O",
        "E0": -0.290,
        "n": 8,
        "delta_H": -45.27,  # Approximate enthalpy for CO₂ reduction to acetate
        "reactants": {"CO2": 2, "H+": 8},
        "products": {"CH3COO-": 1, "H2O": 2},
        "conc": {"CO2": 1e-3, "CH3COO-": 1e-4, "H+": 1e-7}
   } 
]



# Environment definitions
environments = [
    {"name": "alkaline_vent", "pH": 9, "T": 343.15},
    {"name": "acidic_ocean", "pH": 5.5, "T": 313.15},
    {"name": "shallow_pond", "pH": 7, "T": 323.15}
]