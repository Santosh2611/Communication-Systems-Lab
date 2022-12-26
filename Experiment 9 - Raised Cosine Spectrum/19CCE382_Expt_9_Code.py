# PySDR: A Guide to SDR and DSP using Python - https://pysdr.org/content/pulse_shaping.html

import matplotlib.pyplot as plt # Provides an implicit way of plotting
import numpy as np # Support for large, multi-dimensional arrays and matrices
import warnings
warnings.filterwarnings('ignore') # Never print matching warnings

# Compute DFT coefficients using the linear transformation method:    
def DFT(x, plot_name):

    # Compute W(N) 1D Array:
    r1 = c1 = len(x)
    wn = []
    for i in range(r1):
        for j in range(c1):
            wn.append(np.exp(-2j * np.pi * i * j / len(x)))

    # numpy.reshape() is used to give a new shape to an array without changing its data.

    wn_multidim = np.reshape(wn, (r1, c1)) # An N*N W(N) matrix    
    r2 = len(x); c2 = 1
    x_multidim = np.reshape(x, (r2, c2)) # An N*1 x(N) matrix
    
    # Compute X(N) = W(N) * x(N), an N*1 matrix
    fourier_transform_multidim = [[0]*c2]*r1 # NULL Multidimensional Array
    fourier_transform_l_t = [] # Convert Multidimensional Array to 1D
    for i in range(r1):
        for j in range(c2):
            fourier_transform_multidim[i][j] = 0
            for k in range(c1):
                fourier_transform_multidim[i][j] += wn_multidim[i][k] * float(x_multidim[k][j])
            fourier_transform_l_t.append(abs(fourier_transform_multidim[i][j]))
                   
    plt.subplot(1,2,2)
    plt.xlabel("Frequency (f)"); plt.ylabel("Freqeuncy Response, H(f)")
    plt.title(str(plot_name) + "\n" + "in Frequency Domain")
    plt.stem(np.arange(0, len(fourier_transform_l_t)), fourier_transform_l_t)
    plt.grid(True); plt.tight_layout(); plt.show()

# The overlap is fine, as long as your pulse-shaping filter meets this one criterion: all of the pulses must add up to zero at every multiple of our symbol period T, except for one of the pulses.

num_symbols = 10
sps = 8 # 8 samples per symbol
bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0's
x = np.array([])

for bit in bits:
    pulse = np.zeros(sps)
    pulse[0] = bit*2-1 # Set the first value to either a 1 or -1
    x = np.concatenate((x, pulse)) # Add the 8 samples to the signal

plt.figure(); plt.plot(x, '.-')
plt.title("Pulse Train of Impulses")
plt.grid(True); plt.show()

"""
bits: [0, 1, 1, 1, 1, 0, 0, 0, 1, 1]
BPSK symbols: [-1, 1, 1, 1, 1, -1, -1, -1, 1, 1]
Applying 8 samples per symbol: [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, ...]
"""

# Create our raised-cosine filter: -
beta = [0, 0.3, 0.6, 0.9] # Range of β values
for i in range(len(beta)):
    
    Ts = sps # Assume the sample rate is 1 Hz, so the sample period is 1, and the *symbol* period is 8
    t = np.arange(-50, 51) # Remember it's not inclusive of final number
    h = 1/Ts*np.sinc(t/Ts) * np.cos(np.pi*beta[i]*t/Ts) / (1 - (2*beta[i]*t/Ts)**2)
    
    plot_name = "For β = " + str(beta[i])
    plt.figure(); plt.subplot(1,3,1)
    plt.xlabel("Time (t)"); plt.ylabel("Impulse Response, h(t)")
    plt.plot(t, h, '.'); plt.grid(True)
    plt.title(str(plot_name) + "\n" + "in Time Domain")
    
    DFT(h, plot_name)
    
    """
    
    from scipy.fft import fft # Compute the 1-D discrete Fourier Transform    
    y = fft(x); plt.subplot(1,3,2)
    
    plt.xlabel("Frequency (f)"); plt.ylabel("Freqeuncy Response, H(f)")
    plt.title(str(plot_name) + "\n" + "Fast Fourier Transform")
    plt.stem(np.arange(0, len(y)), y); plt.grid(True)
    
    
    from scipy.fft import ifft # Compute the 1-D inverse discrete Fourier Transform
    yinv = ifft(y); plt.subplot(1,3,3)
    
    plt.xlabel("Frequency (f)"); plt.ylabel("Freqeuncy Response, H(f)")
    plt.title(str(plot_name) + "\n" + "Inverse Fast Fourier Transform")
    plt.stem(np.arange(0, len(yinv)), yinv) 
    plt.grid(True); plt.tight_layout(); plt.show()
    
    """
