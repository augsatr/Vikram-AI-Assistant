import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VOICE_DIR = BASE_DIR / "voice"
LOG_FILE = DATA_DIR / "vikram.log"
MEMORY_FILE = DATA_DIR / "memory.faiss"
REMINDERS_FILE = DATA_DIR / "reminders.json"
PERSONALITY_FILE = BASE_DIR / "personality.txt"

PORCUPINE_API_KEY = os.getenv("PORCUPINE_API_KEY", "")
WAKE_WORD_SENSITIVITY = float(os.getenv("WAKE_WORD_SENSITIVITY", "0.5"))
def _get_best_model():
    model = os.getenv("OLLAMA_MODEL", "qwen2.5")
    try:
        import ollama
        client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        available = [m.model.replace(":latest", "") for m in client.list().models]
        if model.replace(":latest", "") in available:
            return model
        for fallback in ["tinyllama", "llama3.2:1b", "phi3:mini"]:
            if fallback in available:
                return fallback
    except:
        pass
    return model

OLLAMA_MODEL = _get_best_model()
VIKRAM_NAME = os.getenv("VIKRAM_NAME", "Vikram")
AUDIO_DEVICE_INDEX = int(os.getenv("AUDIO_DEVICE_INDEX", "-1"))
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
