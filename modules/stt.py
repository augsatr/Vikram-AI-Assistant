import whisper
import numpy as np
import sounddevice as sd
from config import AUDIO_DEVICE_INDEX, AUDIO_SAMPLE_RATE

class SpeechToText:
    def __init__(self, model_size="tiny"):
        print("[STT] Loading Whisper model...")
        self.model = whisper.load_model(model_size)
        print(f"[STT] Whisper {model_size} model loaded (CPU mode)")

    def transcribe(self, duration=5):
        audio = sd.rec(
            int(duration * AUDIO_SAMPLE_RATE),
            samplerate=AUDIO_SAMPLE_RATE,
            channels=1,
            device=AUDIO_DEVICE_INDEX if AUDIO_DEVICE_INDEX >= 0 else None,
        )
        sd.wait()
        audio_np = np.squeeze(audio).astype(np.float32)
        result = self.model.transcribe(audio_np, language="en")
        return result["text"].strip()

    def transcribe_from_file(self, filepath):
        result = self.model.transcribe(filepath, language="en")
        return result["text"].strip()
