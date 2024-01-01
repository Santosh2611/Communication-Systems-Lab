import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

NOISY_SIGNAL_FILE = 'noisy_speech.wav'
CLEAN_SIGNAL_FILE = 'clean_speech.wav'

MAX_AMPLITUDE = 32768.0
NUM_TAPS = 256
STEP_SIZE = 0.01
FORGETTING_FACTOR = 0.99

class LMSFilter:
    def __init__(self, num_taps, step_size):
        self.num_taps = num_taps
        self.step_size = step_size
        self.weights = np.random.rand(num_taps)

    def update(self, signal, target):
        prediction = np.dot(self.weights.T, signal)
        error = target - prediction
        self.weights += self.step_size * error * signal
        return prediction, error

class RLSFilter:
    def __init__(self, num_taps, forgetting_factor):
        self.num_taps = num_taps
        self.forgetting_factor = forgetting_factor
        self.weights = np.random.rand(num_taps)
        self.P = 1e3 * np.eye(num_taps)

    def update(self, signal, target):
        prediction = np.dot(self.weights.T, signal)
        error = target - prediction
        K = np.dot(self.P, signal) / (self.forgetting_factor + np.dot(signal.T, np.dot(self.P, signal)))
        self.weights += K * error
        self.P = (self.P - np.outer(K, np.dot(signal.T, self.P))) / self.forgetting_factor
        return prediction, error

def read_audio_file(file_name):
    """Reads an audio file and returns the sampling rate and signal data."""
    with open(file_name, 'rb') as file:
        rate, signal = wav.read(file)
    signal = signal.astype(np.float32) / MAX_AMPLITUDE
    return rate, signal

def get_magnitude_spectrum(signal, rate):
    """Returns the magnitude spectrum of a signal"""
    freqs, spectrum = signal_spectrum(signal, rate)
    magnitudes = np.abs(spectrum)
    return freqs, magnitudes

def signal_spectrum(signal, rate):
    """Returns the frequency and spectrum of a signal"""
    n = len(signal)
    k = np.arange(n)
    t = n/rate
    freqs = k/t # two sides frequency range
    freqs = freqs[:n//2] # one side frequency range
    sp = np.fft.fft(signal)/n # fft computing and normalization
    sp = sp[:n//2]
    return freqs, sp

def plot_signal_and_spectrum(signal, rate, title):
    """Plots the signal and its frequency spectrum"""
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 8))
    axs[0].plot(signal)
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title(title + ' Audio Signal')
    
    freqs, magnitudes = get_magnitude_spectrum(signal, rate)
    axs[1].plot(freqs, magnitudes)
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_title(title + ' Magnitude Spectrum')
    
    plt.tight_layout()
    plt.show()

def plot_filter_responses(filtered_signal, signal, rate, title):
    """Plots the filter response and the filtered signal"""
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 8))
    axs[0].plot(signal, label='Original Signal', alpha=0.5)
    axs[0].plot(filtered_signal, label='Filtered Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title(title + ' Filtered Audio Signal')
    axs[0].legend()
    
    freqs, magnitudes = get_magnitude_spectrum(signal, rate)
    axs[1].plot(freqs, magnitudes, label='Original Spectrum', alpha=0.5)
    
    freqs, magnitudes = get_magnitude_spectrum(filtered_signal, rate)
    axs[1].plot(freqs, magnitudes, label='Filtered Spectrum')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_title(title + ' Magnitude Spectrum')
    axs[1].legend()
    
    plt.tight_layout()
    plt.show()

def plot_histogram(signal, title):
    """Plots the histogram representation of a signal"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.hist(signal, bins=100)
    ax.set_xlabel('Amplitude')
    ax.set_ylabel('Count')
    ax.set_title('Histogram of ' + title + ' Signal')
    plt.tight_layout()
    plt.show()

def pad_audio_signal(signal, target_len):
    """Pads an audio signal with zeros to match a target length."""
    if len(signal) < target_len:
        padding = target_len - len(signal)
        signal = np.pad(signal, (0, padding), mode='constant')
    return signal[:target_len]

def main():
    # Load audio signals
    rate, noisy_signal = read_audio_file(NOISY_SIGNAL_FILE)
    rate, clean_signal = read_audio_file(CLEAN_SIGNAL_FILE)

    # Normalize signals to have maximum amplitude of 1
    noisy_signal = noisy_signal.astype(np.float32) / MAX_AMPLITUDE
    clean_signal = clean_signal.astype(np.float32) / MAX_AMPLITUDE

    # Pad signals with zeros to match length
    noisy_signal = pad_audio_signal(noisy_signal, len(clean_signal))
    clean_signal = pad_audio_signal(clean_signal, len(noisy_signal))

    # Initialize filters
    lms_filter = LMSFilter(NUM_TAPS, STEP_SIZE)
    rls_filter = RLSFilter(NUM_TAPS, FORGETTING_FACTOR)

    # Apply filters to noisy signal
    lms_output = np.zeros_like(noisy_signal)
    rls_output = np.zeros_like(noisy_signal)
    for i in range(NUM_TAPS, len(noisy_signal)):
        signal_window = noisy_signal[i-NUM_TAPS:i]
        target = clean_signal[i]
        y_lms, e_lms = lms_filter.update(signal_window, target)
        y_rls, e_rls = rls_filter.update(signal_window, target)
        lms_output[i] = y_lms
        rls_output[i] = y_rls

    # Ensure both arrays have the same length
    min_len = min(len(lms_output), len(clean_signal))
    lms_output = lms_output[:min_len]
    clean_signal = clean_signal[:min_len]

    # Calculate the LMS and RLS errors
    lms_error = np.mean((lms_output - clean_signal)**2)
    rls_error = np.mean((rls_output - clean_signal)**2)
    print('LMS error: %.2f' % lms_error)
    print('RLS error: %.2f' % rls_error)

    # Plot results
    plot_signal_and_spectrum(clean_signal, rate, 'Clean')
    plot_signal_and_spectrum(noisy_signal, rate, 'Noisy')
    
    plot_signal_and_spectrum(lms_output, rate, 'LMS')
    plot_signal_and_spectrum(rls_output, rate, 'RLS')
    
    plot_filter_responses(lms_output, noisy_signal, rate, 'LMS')
    plot_filter_responses(rls_output, noisy_signal, rate, 'RLS')
    
    plot_histogram(clean_signal, 'Clean')
    plot_histogram(noisy_signal, 'Noisy')

    # Plot comparison of original and filtered signals
    plt.plot(clean_signal, label='Clean')
    plt.plot(noisy_signal, alpha=0.5, label='Noisy')
    plt.plot(lms_output, label='LMS')
    plt.plot(rls_output, label='RLS')
    plt.title('Comparison of Original and Filtered Signals')
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    main()
