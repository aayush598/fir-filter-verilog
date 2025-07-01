import numpy as np
from scipy.io import wavfile

fs, audio = wavfile.read('example.wav')  # Mono or stereo
audio = audio if audio.ndim == 1 else audio[:, 0]  # Take one channel if stereo
audio = audio[:1000]  # Take first 100 samples
np.savetxt("input_data.txt", audio.astype(np.int16), fmt="%d")
