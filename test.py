import numpy as np
from scipy.optimize import fsolve

# Constants for Cp (kJ/kg.K)
# Values are hypothetical; please replace with actual values from Reid et al as mentioned in the paper
c1_CO2, c2_CO2, c3_CO2, c4_CO2 = 2.0, 0.0, 0.0, 0.0
c1_H2O, c2_H2O, c3_H2O, c4_H2O = 1.0, 0.0, 0.0, 0.0
c1_CO, c2_CO, c3_CO, c4_CO = 1.1, 0.0, 0.0, 0.0
c1_H2, c2_H2, c3_H2, c4_H2 = 0.9, 0.0, 0.0, 0.0
c1_CH4, c2_CH4, c3_CH4, c4_CH4 = 1.5, 0.0, 0.0, 0.0

# Constants for Gibbs free energy calculation (hypothetical values)
a_CO2, b_CO2, c_CO2, d_CO2, e_CO2, f_CO2, g_CO2 = 0, 0, 0, 0, 0, 0, 0
a_H2O, b_H2O, c_H2O, d_H2O, e_H2O, f_H2O, g_H2O = 0, 0, 0, 0, 0, 0, 0
a_CO, b_CO, c_CO, d_CO, e_CO, f_CO, g_CO = 0, 0, 0, 0, 0, 0, 0
a_H2, b_H2, c_H2, d_H2, e_H2, f_H2, g_H2 = 0, 0, 0, 0, 0, 0, 0
a_CH4, b_CH4, c_CH4, d_CH4, e_CH4, f_CH4, g_CH4 = 0, 0, 0, 0, 0, 0, 0

R = 0.008314  # Universal gas constant in kJ/mol.K


def Cp(T, c1, c2, c3, c4):
    return c1 + c2 * T + c3 * T ** 2 + c4 * T ** 3


def gibbs_free_energy(a, b, c, d, e, f, g, T):
    return a + b * T + c * T ** 2 + d * T ** 3 + e / T + f * np.log(T) + g


def equilibrium_constants(T):
    delta_G_boudouard = gibbs_free_energy(a_CO2, b_CO2, c_CO2, d_CO2, e_CO2, f_CO2, g_CO2, T) - gibbs_free_energy(a_CO,
                                                                                                                  b_CO,
                                                                                                                  c_CO,
                                                                                                                  d_CO,
                                                                                                                  e_CO,
                                                                                                                  f_CO,
                                                                                                                  g_CO,
                                                                                                                  T)
    delta_G_water_gas = gibbs_free_energy(a_H2O, b_H2O, c_H2O, d_H2O, e_H2O, f_H2O, g_H2O, T) + gibbs_free_energy(a_CO,
                                                                                                                  b_CO,
                                                                                                                  c_CO,
                                                                                                                  d_CO,
                                                                                                                  e_CO,
                                                                                                                  f_CO,
                                                                                                                  g_CO,
                                                                                                                  T) - gibbs_free_energy(
        a_H2, b_H2, c_H2, d_H2, e_H2, f_H2, g_H2, T)
    delta_G_shift = gibbs_free_energy(a_H2O, b_H2O, c_H2O, d_H2O, e_H2O, f_H2O, g_H2O, T) + gibbs_free_energy(a_CO,
                                                                                                              b_CO,
                                                                                                              c_CO,
                                                                                                              d_CO,
                                                                                                              e_CO,
                                                                                                              f_CO,
                                                                                                              g_CO,
                                                                                                              T) - gibbs_free_energy(
        a_H2, b_H2, c_H2, d_H2, e_H2, f_H2, g_H2, T) - gibbs_free_energy(a_CO2, b_CO2, c_CO2, d_CO2, e_CO2, f_CO2,
                                                                         g_CO2, T)
    delta_G_methanation = gibbs_free_energy(a_CH4, b_CH4, c_CH4, d_CH4, e_CH4, f_CH4, g_CH4, T) - gibbs_free_energy(
        a_CO, b_CO, c_CO, d_CO, e_CO, f_CO, g_CO, T) - gibbs_free_energy(a_H2, b_H2, c_H2, d_H2, e_H2, f_H2, g_H2, T)

    K_boudouard = np.exp(-delta_G_boudouard / (R * T))
    K_water_gas = np.exp(-delta_G_water_gas / (R * T))
    K_shift = np.exp(-delta_G_shift / (R * T))
    K_methanation = np.exp(-delta_G_methanation / (R * T))

    return K_boudouard, K_water_gas, K_shift, K_methanation


def mass_balance(x, *args):
    T, C, H, O = args
    x_CO2, x_H2O, x_CO, x_H2, x_CH4 = x
    K_boudouard, K_water_gas, K_shift, K_methanation = equilibrium_constants(T)

    # Equilibrium equations
    eq1 = x1 * x4 / (x3 * x2) - K_shift  # Water-gas shift reaction
    eq2 = x1 / (C - x3 - x4) - K_boudouard  # Boudouard reaction
    eq3 = x2 / (H - 2*x5) - K_water_gas  # Water gas reaction
    eq4 = x5 / (C - x3 - x4) - K_methanation  # Methanation reaction

    # Mass balance equations
    eq5 = x_CO2 + x_H2O + x_CO + x_H2 + x_CH4 - 1

    return [eq1, eq2, eq3, eq4, eq5]


def syngas_composition(T, C, H, O):
    initial_guess = [0.2, 0.2, 0.2, 0.2, 0.2]  # Initial guess for the fsolve
    result = fsolve(mass_balance, initial_guess, args=(T, C, H, O))
    return result


# Example usage with hypothetical values for C, H, O (from ultimate analysis of biomass)
temperature = 1073  # 800°C in Kelvin
C, H, O = 0.3, 0.05, 0.35  # Example CHON composition

composition = syngas_composition(temperature, C, H, O)
print("Syngas Composition (CO2, H2O, CO, H2, CH4):", composition)
