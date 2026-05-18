import sounddevice as sd
import numpy as np
import whisper

rec = sd.rec(int(16000 * 3), samplerate=16000, channels=1)
sd.wait()
audio = np.squeeze(rec).astype(np.float32)

mx = float(np.max(np.abs(audio)))
print("dtype was:", rec.dtype)
print(f"Max: {mx:.6f}")
print(f"Mean RMS: {float(np.sqrt(np.mean(audio**2)))*1000:.4f}")

model = whisper.load_model("tiny")
result = model.transcribe(audio, language="en")
print(f"Whisper: [{result['text'].strip()}]")
