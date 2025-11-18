import math

# Constants
F = 96485.3329  # Faraday's constant (C/mol)
R = 8.3145      # Universal gas constant (J/mol·K)


def calculate_Q(pair):
    Q = 1.0
    for species, coeff in pair["products"].items():
        conc = pair["conc"].get(species, 1)
        Q *= conc ** coeff
    for species, coeff in pair["reactants"].items():
        conc = pair["conc"].get(species, 1)
        Q /= conc ** coeff
    return Q


def adjust_E0(E0, n, T, Q):
    return E0 - (R * T) / (n * F) * math.log(Q)


def calculate_deltaG(E, n):
    return -n * F * E


def calculate_exergy_efficiency_from_G(deltaG, max_deltaG):
    if max_deltaG == 0:
        return 0.0
    return (deltaG / max_deltaG) * 100


def calculate_exergy_efficiency_from_H(deltaG, deltaH_kJ):
    """
    Calculates exergy efficiency from ΔG and ΔH.

    Returns a value capped between 0% and 100% to prevent unphysical results.
    If ΔH is zero or signs are incompatible, returns np.nan.
    """
    if abs(deltaH_kJ) < 1e-8:
        return float('nan')  # undefined for ΔH = 0

    deltaH_J = deltaH_kJ * 1000

    # Only allow physically meaningful results (ΔG must be positive, ΔH must be positive)
    raw_eff = deltaG / deltaH_J

    if raw_eff < 0:
        return 0.0  # treat negative efficiency as 0%
    elif raw_eff > 1:
        return 100.0  # cap at 100%
    else:
        return raw_eff * 100


if __name__ == "__main__":
    print("Thermodynamics module with ΔH-based exergy modeling loaded.")