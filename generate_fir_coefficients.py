import numpy as np
from scipy.signal import firwin
import matplotlib.pyplot as plt

# FIR filter design
num_taps = 8                # 8-tap FIR filter as in your Verilog
cutoff_hz = 10              # cutoff frequency (Hz)
sample_rate = 100           # match the sampling rate used for your signal

# Generate low-pass FIR filter coefficients
coeffs = firwin(num_taps, cutoff_hz, fs=sample_rate, window='hamming')

# Normalize and scale for fixed-point (16-bit signed)
coeffs_scaled = np.round(coeffs * (2**12)).astype(np.int16)

# Save to file (optional)
np.savetxt("fir_coeffs.txt", coeffs_scaled, fmt="%d")

# Print Verilog-ready format
print("// Verilog Coefficients")
for i, c in enumerate(coeffs_scaled):
    print(f"coeff[{i}] = 16'sd{c};")

# Optional plot
plt.stem(coeffs, use_line_collection=True)
plt.title("FIR Filter Coefficients (Low-pass)")
plt.xlabel("Tap")
plt.ylabel("Coefficient Value")
plt.grid(True)
plt.tight_layout()
plt.savefig("fir_coeff_plot.png")
plt.show()
