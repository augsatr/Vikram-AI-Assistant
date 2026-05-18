import os, time
os.add_dll_directory(os.path.join(os.environ["TEMP"], "ffmpeg-shared", "ffmpeg-8.1.1-full_build-shared", "bin"))
from TTS.api import TTS

print("Loading XTTS...")
t0 = time.time()
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
print(f"Loaded in {time.time()-t0:.0f}s")

print("Generating short text...")
t0 = time.time()
tts.tts_to_file(text="Hello boss, Vikram is online", speaker_wav="voice/madara_full.wav", language="en", file_path="voice/_bench_out.wav")
dt = time.time() - t0
print(f"Generated in {dt:.0f}s")
sz = os.path.getsize("voice/_bench_out.wav")
print(f"File: {sz/1024:.0f} KB")
print(f"Real-time ratio: {dt / (sz/16000/2):.1f}x (1.0 = realtime)")
