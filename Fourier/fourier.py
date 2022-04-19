# Periodic signal expansion into fourier series
# Input to the program is one period of a sampled signal
# Number of samples doesn't matter, but they have to be evenly spaced

import numpy as np

def fourier(data, num_coeff):
    # Variables
    vals = np.array(data)
    args = np.array([x for x in range(1, len(data) + 1)])
    period = args[-1]
    ω = 2*np.pi/period

    # Calculate step and mean value
    Δ = args[0]
    mean_val = np.mean(vals)
    vals = np.subtract(vals, mean_val)

    # Calculate Fourier series coefficients as:
    #   ak = 2/T * integral from 0 to T of: f(t)*cos(k ω0 t) dt
    #   bk = 2/T * integral from 0 to T of: f(t)*sin(k ω0 t) dt
    a_coeff = []
    b_coeff = []

    # Simplest integral approximation
    for k in range(1, num_coeff + 1):
        a_coeff.append(2 / period * Δ * np.sum(np.multiply(vals, np.cos(k*ω*args))))
        b_coeff.append(2 / period * Δ * np.sum(np.multiply(vals, np.sin(k*ω*args))))

    # Return a and b coefficients
    return a_coeff, b_coeff, mean_val