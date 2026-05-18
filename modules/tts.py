import asyncio
import threading
import tempfile
import os
from pathlib import Path
from config import VOICE_DIR

_FFMPEG_DLL_DIR = os.path.join(os.environ.get("TEMP", ""), "ffmpeg-shared", "ffmpeg-8.1.1-full_build-shared", "bin")
if os.path.isdir(_FFMPEG_DLL_DIR):
    os.add_dll_directory(_FFMPEG_DLL_DIR)

class TextToSpeech:
    def __init__(self, use_cloned_voice=False):
        self.tts_engine = None
        self.voice = "en-US-GuyNeural"
        self.speaker_wav = None

        wav_files = list(VOICE_DIR.glob("*.wav")) + list(VOICE_DIR.glob("*.mp3"))
        if wav_files:
            self.speaker_wav = str(wav_files[0])
            print(f"[TTS] Voice sample found: {wav_files[0].name}")

        if use_cloned_voice and self.speaker_wav:
            self._load_xtts()
        else:
            self._load_edge()
            if use_cloned_voice and not self.speaker_wav:
                print("[TTS] No voice sample found in voice/ folder")
                print("[TTS] Run record_voice.py to record your voice")

    def _load_xtts(self):
        try:
            from TTS.api import TTS
            self.tts_engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
            self.use_xtts = True
            print("[TTS] XTTS v2 voice cloning loaded")
        except Exception as e:
            print(f"[TTS] XTTS not available: {e}")
            print("[TTS] Install with: pip install TTS")
            print("[TTS] Falling back to edge-tts neural voice")
            self._load_edge()

    def _load_edge(self):
        self.use_xtts = False
        self.tts_engine = None

    def speak(self, text):
        def _play():
            try:
                if self.use_xtts and self.tts_engine and self.speaker_wav:
                    self._speak_xtts(text)
                else:
                    self._speak_edge(text)
            except Exception as e:
                print(f"[TTS] Error: {e}")
                self._speak_fallback(text)

        threading.Thread(target=_play, daemon=True).start()

    def _speak_xtts(self, text):
        from TTS.api import TTS
        out_path = os.path.join(tempfile.gettempdir(), "_vikram_tts.wav")
        self.tts_engine.tts_to_file(text=text, speaker_wav=self.speaker_wav, language="en", file_path=out_path)
        import winsound
        winsound.PlaySound(out_path, winsound.SND_FILENAME)
        os.unlink(out_path)

    def _speak_edge(self, text):
        import edge_tts
        import winsound
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tts = edge_tts.Communicate(text, self.voice)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            loop.run_until_complete(tts.save(f.name))
            tmp_path = f.name
        winsound.PlaySound(tmp_path, winsound.SND_FILENAME)
        os.unlink(tmp_path)

    def _speak_fallback(self, text):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            print(f"[VIKRAM] {text}")

    def say(self, text):
        self.speak(text)
