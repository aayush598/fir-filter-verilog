import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from scipy.signal import firwin

# ------------------- Signal Parameters -------------------
samples = 1000
amplitude = 1000
frequency = 5         # Signal frequency (Hz)
noise_level = 300     # Gaussian noise level
sample_rate = 100     # Sampling frequency (Hz)

# ------------------- Generate Noisy Signal -------------------
t = np.linspace(0, 1, samples, endpoint=False)
signal = amplitude * np.sin(2 * np.pi * frequency * t)
noise = np.random.normal(0, noise_level, samples)
noisy_signal = signal + noise
noisy_signal_int16 = noisy_signal.astype(np.int16)

# Save signal to text file
np.savetxt("input_data.txt", noisy_signal_int16, fmt="%d")

# ------------------- FIR Filter Design -------------------
num_taps = 8
cutoff_hz = 10  # Low-pass cutoff

# Design low-pass filter using Hamming window
coeffs = firwin(num_taps, cutoff_hz, fs=sample_rate, window='hamming')

# Scale to fixed-point (multiply by 2^12 and round)
coeffs_scaled = np.round(coeffs * (2**12)).astype(np.int16)
np.savetxt("fir_coeffs.txt", coeffs_scaled, fmt="%d")

# ------------------- Verilog Coefficient Print -------------------
print("\n// Verilog Coefficients")
for i, c in enumerate(coeffs_scaled):
    print(f"coeff[{i}] = 16'sd{c};")

# ------------------- Optional Plot -------------------
plt.figure(figsize=(10, 4))
plt.plot(t, signal, label="Original Signal", linewidth=2)
plt.plot(t, noisy_signal, label="Noisy Signal", alpha=0.6)
plt.title("Noisy Signal for FIR Filter Test")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("noisy_signal_plot.png")
plt.show()

# Plot FIR filter coefficients
plt.figure(figsize=(6, 3))
plt.stem(coeffs_scaled, use_line_collection=True)
plt.title("Scaled FIR Filter Coefficients")
plt.xlabel("Tap Index")
plt.ylabel("Coefficient Value (Q12)")
plt.grid(True)
plt.tight_layout()
plt.savefig("fir_coeff_plot.png")
plt.show()
