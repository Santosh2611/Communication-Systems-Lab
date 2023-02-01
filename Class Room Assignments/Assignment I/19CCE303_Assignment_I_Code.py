import librosa # Python package for music and audio analysis
import matplotlib.pyplot as plt # Collection of command style functions that make matplotlib work like MATLAB
import numpy as np # Support for large, multi-dimensional arrays and matrices

y, sampling_rate = librosa.load('Impact_Moderato.wav', sr=41200, mono=False) # Load an audio file as a floating point time series
ts = 1/len(y[1]) # Choose sampling rate
x = np.arange(0,1,ts) # Return evenly spaced values within a given interval
print("\nTo perform quantization:\nMinimmum Value: " + str((min(y[1]))) + "\nMaximum Value: " + str((max(y[1]))))

# Plot Audio File: -
plt.plot(x,y[1])
plt.title("Sampled Version of Audio File")
plt.xlabel("Time (t)"); plt.ylabel("Amplitude (A)")
plt.grid(True); plt.show()

encoding_delta = []
delta = 0.01 # Initial Delta Value

# Perform Delta Modulation: -
for i in range(len(y[1])):
    
    if delta < y[1][i]:
        encoding_delta.append(0)
        delta = delta + 0.01
    
    else:
        encoding_delta.append(1)
        delta = delta - 0.01
print("\nLength of Encoded Data Array: ", len(encoding_delta))        
print("First 50 Encoded Data: ", encoding_delta[0:50])

start = -0.3
quantization_levels = []
quantization_levels.append(start)

# Perform 128-Level Quantization: -
for i in range(128):
    start = start + 0.0047
    quantization_levels.append(start)
print("\nNumber of Quantization Levels: ", len(quantization_levels))
print("First 50 Quantization Levels: ", quantization_levels[0:50])

quantized_values = []
for i in range(len(quantization_levels)-1):
    temp = (quantization_levels[i]+quantization_levels[i+1])/2
    quantized_values.append(temp)
print("\nNumber of Quantized Values: ", len(quantized_values))
print("First 50 Quantized Values: ", quantized_values[0:50])

encoding = encoded_signal = []
for i in range(len(y[1])):    
    flag = 0    
    for j in range(len(quantized_values)):
        
        if y[1][i]<quantized_values[j]:
            encoding.append(j+1)
            encoded_signal.append(bin(j+1))
            flag = 1
        
        if flag == 1:
            break
print("\nLength of Encoded Signal Array: ", len(encoded_signal))        
print("First 50 Encoded Signal: ", encoded_signal[0:50])

delta = 0.01 # Initial Delta Value
reconstruction = reconstruction_delta = []

# Perform Reconstruction for the Encoded Binary Numbers:
for i in range(len(encoding_delta)):
    if encoding_delta[i] == 0:
        delta = delta + 0.001
        reconstruction_delta.append(delta)
    else:
        delta = delta - 0.001
        reconstruction_delta.append(delta)

plt.plot(x, reconstruction_delta)
plt.title("Reconstructed Audio File from the Encoded Binary Numbers")
plt.xlabel("Time (t)"); plt.ylabel("Amplitude (A)")
plt.grid(True); plt.show()
