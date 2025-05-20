# This script generates plots for the optimal conditions of redox pairs based on the results from the optimization process.
# It includes functions to plot optimal exergy efficiency, scatter plots of optimal conditions, and bar plots of ΔG at optimal conditions.
# It also ensures that the figures directory exists before saving the plots.

import math

# Constants
F = 96485.3329  # Faraday's constant (C/mol)
R = 8.3145      # Universal gas constant (J/mol·K)


def calculate_Q(pair):
    """
    Calculates the reaction quotient Q using given concentrations and stoichiometry.
    """
    Q = 1.0
    for species, coeff in pair["products"].items():
        conc = pair["conc"].get(species, 1)
        Q *= conc ** coeff
    for species, coeff in pair["reactants"].items():
        conc = pair["conc"].get(species, 1)
        Q /= conc ** coeff
    return Q


def adjust_E0(E0, n, T, Q):
    """
    Adjusts the standard potential E0 using the Nernst equation.
    """
    return E0 - (R * T) / (n * F) * math.log(Q)


def calculate_deltaG(E, n):
    """
    Calculates the Gibbs free energy change ΔG.
    """
    return -n * F * E


def calculate_exergy_efficiency_from_G(deltaG, max_deltaG):
    """
    Estimates the exergy efficiency using ΔG and ΔG⁰.
    """
    if max_deltaG == 0:
        return 0.0
    return (deltaG / max_deltaG) * 100


def calculate_exergy_efficiency_from_H(deltaG, deltaH_kJ):
    """
    Estimates the exergy efficiency using ΔG and ΔH.
    """
    if deltaH_kJ == 0:
        return 0.0
    deltaH_J = deltaH_kJ * 1000
    return (deltaG / deltaH_J) * 100


# Optional self-test
if __name__ == "__main__":
    print("Thermodynamics module with ΔH-based exergy modeling loaded.")