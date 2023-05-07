import numpy as np
import matplotlib.pyplot as plt
import spectral

# Define grid
t_max = 10
N = 100
t = np.linspace(0,10,N)
Delta = t_max / N

# Define function
h = np.exp(-(t - t_max/2)**2) # Gaussian

# Computing the derivative
H = spectral.fft(h)
f = spectral.fftfreq(len(t), Delta)
H_dot = 2 * np.pi * 1j * f * H
h_dot = spectral.ifft(H_dot)

# Plot results
plt.plot(t, h, label=f'$h(t)$')
plt.plot(t, h_dot, label=f'$\dot h(t)$')
plt.plot(t, - 2 * (t - t_max/2) * np.exp(-(t - t_max/2)**2), label=f'expected $\dot h(t)$', linestyle='dashed')
plt.legend()
plt.show()
