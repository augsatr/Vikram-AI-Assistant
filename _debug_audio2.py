import sounddevice as sd
import numpy as np

devices_to_try = [
    (1, "MME - Microphone Array"),
    (5, "DirectSound - Microphone Array"),
    (9, "WASAPI - Microphone Array"),
    (20, "WDM-KS - Realtek Mic input"),
]

for dev_idx, name in devices_to_try:
    try:
        info = sd.query_devices(dev_idx)
        sr = int(info["default_samplerate"])
        rec = sd.rec(int(sr * 2), samplerate=sr, channels=1, device=dev_idx)
        sd.wait()
        audio = np.squeeze(rec).astype(np.float32)
        mx = float(np.max(np.abs(audio)))
        rms = float(np.sqrt(np.mean(audio ** 2)))
        print(f"[{dev_idx}] {name}: Max={mx:.6f}, RMS={rms*1000:.4f}")
    except Exception as e:
        print(f"[{dev_idx}] {name}: ERROR {e}")
