# This script generates plots for the optimal conditions of redox pairs based on the results from the optimization process.
# It includes functions to plot optimal exergy efficiency, scatter plots of optimal conditions, and bar plots of ΔG at optimal conditions.
# It also ensures that the figures directory exists before saving the plots.

# Redox pairs (12 total) with standard potentials, stoichiometry, concentrations, and ΔH
redox_pairs = [
    {
        "name": "H2/H+",
        "reaction": "2H+ + 2e- → H2",
        "E0": -0.414,
        "n": 2,
        "delta_H": -286,  # kJ/mol
        "reactants": {"H+": 2},
        "products": {"H2": 1},
        "conc": {"H+": 1e-7, "H2": 1e-6}
    },
    {
        "name": "CO2/CH4",
        "reaction": "CO2 + 8H+ + 8e- → CH4 + 2H2O",
        "E0": -0.244,
        "n": 8,
        "delta_H": -891,  # kJ/mol (approx. combustion of CH4)
        "reactants": {"CO2": 1, "H+": 8},
        "products": {"CH4": 1},
        "conc": {"CO2": 1e-3, "CH4": 1e-6, "H+": 1e-7}
    },
    {
        "name": "NO3-/NO2-",
        "reaction": "NO3⁻ + 2H⁺ + 2e⁻ → NO2⁻ + H2O",
        "E0": 0.421,
        "n": 2,
        "delta_H": -117,  # estimated
        "reactants": {"NO3-": 1, "H+": 2},
        "products": {"NO2-": 1},
        "conc": {"NO3-": 1e-4, "NO2-": 1e-6, "H+": 1e-7}
    },
    {
        "name": "SO4^2-/H2S",
        "reaction": "SO₄²⁻ + 8H⁺ + 8e⁻ → H₂S + 4H₂O",
        "E0": -0.217,
        "n": 8,
        "delta_H": -797,  # Approximate enthalpy for sulfate reduction
        "reactants": {"SO4^2-": 1, "H+": 8},
        "products": {"H2S": 1, "H2O": 4},
        "conc": {"SO4^2-": 1e-3, "H2S": 1e-6, "H+": 1e-7}
    },
    {
        "name": "NO2^-/N2",
        "reaction": "2NO₂⁻ + 6H⁺ + 6e⁻ → N₂ + 2H₂O",
        "E0": 0.34,
        "n": 6,
        "delta_H": -1020,  # Estimate based on full denitrification
        "reactants": {"NO2-": 2, "H+": 6},
        "products": {"N2": 1, "H2O": 2},
        "conc": {"NO2-": 1e-4, "N2": 1e-6, "H+": 1e-7}
    },
    {
        "name": "Acetate/CO2",
        "reaction": "CH₃COO⁻ + 2H₂O → 2CO₂ + 7H⁺ + 8e⁻",
        "E0": -0.290,
        "n": 8,
        "delta_H": -870,  # Rough enthalpy for acetate oxidation
        "reactants": {"Acetate": 1},
        "products": {"CO2": 2},
        "conc": {"Acetate": 1e-4, "CO2": 1e-3}
    },
]



# Environment definitions
environments = [
    {"name": "alkaline_vent", "pH": 9, "T": 343.15},
    {"name": "acidic_ocean", "pH": 5.5, "T": 313.15},
    {"name": "shallow_pond", "pH": 7, "T": 323.15}
]