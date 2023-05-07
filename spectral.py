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
