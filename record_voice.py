import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from pathlib import Path

VOICE_DIR = Path(__file__).parent / "voice"
VOICE_DIR.mkdir(exist_ok=True)

print("=" * 50)
print("  Record your voice for Vikram")
print("=" * 50)
print("\nSpeak naturally for 30 seconds.")
print("Try: 'Hello, I am your creator. Vikram, welcome to the team.'")
print("\nRecording will start in 3 seconds...")

import time
time.sleep(3)

fs = 16000
duration = 30
print(f"\nRecording {duration} seconds... Speak now!")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

out_path = VOICE_DIR / "my_voice.wav"
wav.write(str(out_path), fs, np.int16(audio * 32767))
print(f"\nSaved to: {out_path}")
print(f"Size: {out_path.stat().st_size / 1024:.1f} KB")

print("\nDone! Run 'python vikram.py' and it will use your voice.")
