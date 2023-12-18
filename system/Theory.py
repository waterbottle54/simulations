import numpy as np

def y_a(t, number_a, number_b, fatality_a, fatality_b):
    y_a0 = number_a
    y_b0 = number_b
    k_a = fatality_a
    k_b = fatality_b
    spd = np.sqrt(k_a * k_b)
    rt = np.sqrt(k_b / k_a)
    return y_a0 * np.cosh(spd * t) - y_b0 * rt * np.sinh(spd * t)

def y_b(t, number_a, number_b, fatality_a, fatality_b):
    y_a0 = number_a
    y_b0 = number_b
    k_a = fatality_a
    k_b = fatality_b
    spd = np.sqrt(k_a * k_b)
    rt = np.sqrt(k_a / k_b)
    return y_b0 * np.cosh(spd * t) - y_a0 * rt * np.sinh(spd * t)