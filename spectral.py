import numpy as np

def fft(h):
	H = np.fft.fft(h)
	return H

def ifft(H):
	h = np.fft.ifft(H)
	return h

def fftfreq(N, Delta):
	f = np.fft.fftfreq(N, Delta)
	return f

def derivative(h, N, Delta):
	H = fft(h)
	f = fftfreq(N, Delta)
	H_prime = 2 * np.pi * 1j * f * H
	h_prime = ifft(H_prime)
	return h_prime.real
