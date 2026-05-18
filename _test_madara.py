import os
ffmpeg_dll_dir = os.path.join(os.environ.get("TEMP", ""), "ffmpeg-shared", "ffmpeg-8.1.1-full_build-shared", "bin")
if os.path.isdir(ffmpeg_dll_dir):
    os.add_dll_directory(ffmpeg_dll_dir)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from TTS.api import TTS
from pathlib import Path
import time

voice_dir = Path(__file__).parent / "voice"
madara_wav = voice_dir / "madara_full.wav"

if not madara_wav.exists():
    print(f"ERROR: {madara_wav} not found!")
    exit(1)

import builtins
original_input = builtins.input
builtins.input = lambda prompt="": "y"

print("Loading XTTS v2 model (first time downloads ~2GB)...")
start = time.time()
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
builtins.input = original_input
print(f"Model loaded in {time.time()-start:.1f}s")

print(f"Cloning voice from: {madara_wav}")
out = voice_dir / "madara_test_output.wav"
tts.tts_to_file(
    text="I am Vikram, your personal assistant. I am the strongest of all time.",
    speaker_wav=str(madara_wav),
    language="en",
    file_path=str(out)
)

print(f"Test audio saved: {out}")
print(f"Size: {out.stat().st_size / 1024:.1f} KB")
print("SUCCESS! Madara voice cloned!")
