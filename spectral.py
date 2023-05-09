import numpy as np

# Reference variables (with default values)
N_ref = 101
x_min_ref = 0
x_max_ref = 10

# Grid variables (with default values)
x = np.linspace(x_min_ref, x_max_ref, N_ref, endpoint=False)
Delta = (x_max_ref - x_min_ref) / N_ref
f = np.fft.fftfreq(N_ref, Delta)

def grid(N, x_min, x_max):
	global N_ref, x_min_ref, x_max_ref, x, Delta, f
	N_ref = N
	x_min_ref = x_min
	x_max_ref = x_max
	
	x = np.linspace(x_min, x_max, N, endpoint=False)
	Delta = (x_max - x_min) / N
	f = np.fft.fftfreq(N, Delta)

	return x, Delta

def derivative(h):
	H = np.fft.fft(h)

	H_prime = 2 * np.pi * 1j * f * H
	h_prime = np.fft.ifft(H_prime)
	
	return h_prime.real

def logistic_low_pass(fmag, cutoff, width):
	return 1./(1. + np.exp((fmag-cutoff)/width))

def filter(h):
	H = np.fft.fft(h)

	fmag = np.abs(f)
	cutoff = .7*np.max(f)
	width = .05*np.max(f)
	H *= logistic_low_pass(fmag, cutoff, width)

	h = np.fft.ifft(H).real
	return h
