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
        "name": "Fe3+/Fe2+",
        "reaction": "Fe3+ + e- → Fe2+",
        "E0": 0.77,
        "n": 1,
        "delta_H": -20,  # estimated
        "reactants": {"Fe3+": 1},
        "products": {"Fe2+": 1},
        "conc": {"Fe3+": 1e-4, "Fe2+": 1e-3}
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
        "name": "S0/H2S",
        "reaction": "S⁰ + 2H⁺ + 2e⁻ → H2S",
        "E0": 0.14,
        "n": 2,
        "delta_H": -33,  # kJ/mol approx.
        "reactants": {"S0": 1, "H+": 2},
        "products": {"H2S": 1},
        "conc": {"S0": 1e-5, "H2S": 1e-6, "H+": 1e-7}
    },
    {
        "name": "CO2/CO",
        "reaction": "CO2 + 2H⁺ + 2e⁻ → CO + H2O",
        "E0": -0.106,
        "n": 2,
        "delta_H": -199,  # kJ/mol approx.
        "reactants": {"CO2": 1, "H+": 2},
        "products": {"CO": 1},
        "conc": {"CO2": 1e-3, "CO": 1e-6, "H+": 1e-7}
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
        "name": "MnO2/Mn2+",
        "reaction": "MnO₂ + 4H⁺ + 2e⁻ → Mn²⁺ + 2H₂O",
        "E0": 1.23,
        "n": 2,
        "delta_H": -520,  # Estimate based on Mn redox energetics
        "reactants": {"MnO2": 1, "H+": 4},
        "products": {"Mn2+": 1, "H2O": 2},
        "conc": {"MnO2": 1e-4, "Mn2+": 1e-3, "H+": 1e-7}
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
    {
        "name": "Formate/CO2",
        "reaction": "HCOO⁻ → CO₂ + H⁺ + 2e⁻",
        "E0": -0.43,
        "n": 2,
        "delta_H": -254,  # Enthalpy for formate oxidation
        "reactants": {"Formate": 1},
        "products": {"CO2": 1},
        "conc": {"Formate": 1e-4, "CO2": 1e-3}
    },
    {
        "name": "H2O2/H2O",
        "reaction": "H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O",
        "E0": 1.77,
        "n": 2,
        "delta_H": -191,  # Decomposition enthalpy of H2O2
        "reactants": {"H2O2": 1},
        "products": {"H2O": 1, "O2": 0.5},
        "conc": {"H2O2": 1e-5, "H2O": 1, "O2": 1e-6}
    }
]



# Environment definitions
environments = [
    {"name": "alkaline_vent", "pH": 9, "T": 343.15},
    {"name": "acidic_ocean", "pH": 5.5, "T": 313.15},
    {"name": "shallow_pond", "pH": 7, "T": 323.15}
]