import sounddevice as sd
import numpy as np
from openwakeword import Model

m = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

print("Recording 4 seconds... say 'hey jarvis' now!")
fs = 16000
rec = sd.rec(int(fs * 4), samplerate=fs, channels=1, dtype="float32")
sd.wait()
audio = rec[:, 0]

scores = []
for i in range(0, len(audio) - 1280, 1280):
    chunk = audio[i : i + 1280]
    pred = m.predict(chunk)
    scores.append(pred["hey_jarvis"])

max_score = max(scores)
print(f"Max score: {max_score:.4f}")
print(f"Non-zero scores: {sum(1 for s in scores if s > 0)}/{len(scores)}")
print(f"Scores > 0.1: {sum(1 for s in scores if s > 0.1)}")
print(f"Scores > 0.3: {sum(1 for s in scores if s > 0.3)}")
