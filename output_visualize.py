import matplotlib.pyplot as plt  # type: ignore

# Read input data
with open("input_data.txt", "r") as f:
    input_data = [int(line.strip()) for line in f if line.strip()]

# Read output data
with open("output_data.txt", "r") as f:
    output_data = [int(line.strip()) for line in f if line.strip()]

# Determine input range
min_in = min(input_data)
max_in = max(input_data)

# Normalize and rescale output to match input range
min_out = min(output_data)
max_out = max(output_data)

scaled_output = [
    ((y - min_out) / (max_out - min_out)) * (max_in - min_in) + min_in
    for y in output_data
] if max_out != min_out else [min_in for _ in output_data]

# X-axes
input_x = list(range(len(input_data)))
output_x = list(range(len(scaled_output)))

# Plot on two subplots
plt.figure(figsize=(10, 8))

# Top: Input Signal
plt.subplot(2, 1, 1)
plt.plot(input_x, input_data, label="Input Signal", marker='o', color='blue')
plt.title("FIR Filter - Input Signal")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()

# Bottom: FIR Filter Output
plt.subplot(2, 1, 2)
plt.plot(output_x, scaled_output, label="Scaled FIR Output", marker='s', color='green')
plt.title("FIR Filter - Scaled Output Signal")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("fir_input_vs_output.png")  # Save the figure
plt.show()
