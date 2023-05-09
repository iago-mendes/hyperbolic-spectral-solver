import numpy as np

def derivative(h, N, Delta):
	H = np.fft.fft(h)
	f = np.fft.fftfreq(N, Delta)
	H_prime = 2 * np.pi * 1j * f * H
	h_prime = np.fft.ifft(H_prime)
	return h_prime.real
