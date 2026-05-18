import sounddevice as sd

print("Default input device:", sd.default.device)
print()

print("Input devices:")
devices = sd.query_devices()
for i, d in enumerate(devices):
    if d["max_input_channels"] > 0:
        print(f'  [{i}] {d["name"]} - {d["default_samplerate"]}Hz')

print()

# Test recording with explicit device
print("Testing recording on default device...")
rec = sd.rec(int(16000 * 2), samplerate=16000, channels=1, dtype="float32")
sd.wait()
import numpy as np
rms = float(np.sqrt(np.mean(rec**2)))
print(f"RMS level (default device): {rms*1000:.2f}")
print(f"Max sample: {float(np.max(np.abs(rec))):.4f}")
