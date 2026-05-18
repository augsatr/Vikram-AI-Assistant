import sounddevice as sd
print("Output devices:")
for i, d in enumerate(sd.query_devices()):
    if d["max_output_channels"] > 0:
        print(f"  [{i}] {d['name']}")
print(f"Default output index: {sd.default.device[1]}")

import winsound
# Try playing a simple beep
import numpy as np
sr = 44100
t = 1.0
freq = 440
samples = (np.sin(2 * np.pi * np.arange(int(sr * t)) * freq / sr) * 32767 * 0.3).astype(np.int16)
import struct, tempfile, os
path = os.path.join(tempfile.gettempdir(), "_test_beep.wav")
with open(path, "wb") as f:
    f.write(b"RIFF")
    import struct
    data_size = len(samples) * 2
    f.write(struct.pack("<I", 36 + data_size))
    f.write(b"WAVE")
    f.write(b"fmt ")
    f.write(struct.pack("<I", 16))
    f.write(struct.pack("<HH", 1, 1))
    f.write(struct.pack("<I", sr))
    f.write(struct.pack("<I", sr * 2))
    f.write(struct.pack("<HH", 2, 16))
    f.write(b"data")
    f.write(struct.pack("<I", data_size))
    f.write(samples.tobytes())

print(f"Playing beep from {path}")
winsound.PlaySound(path, winsound.SND_FILENAME)
print("Beep played - did you hear it?")
os.unlink(path)
