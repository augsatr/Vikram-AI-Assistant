import sys
import time
import json
import threading
import signal
from pathlib import Path
from datetime import datetime

from config import (
    BASE_DIR, DATA_DIR, VIKRAM_NAME, OLLAMA_MODEL,
)
from modules.wake_word import WakeWordDetector
from modules.stt import SpeechToText
from modules.brain import Brain
from modules.tts import TextToSpeech
from modules.actions import ActionEngine
from modules.memory import Memory


class VikramAssistant:
    def __init__(self):
        print(f"{'='*50}")
        print(f"  {VIKRAM_NAME} v1.0 - Your AI Assistant")
        print(f"{'='*50}")
        print(f"  Model: {OLLAMA_MODEL}")
        print(f"{'='*50}\n")

        self.running = True
        self.listening = False
        self.system_prompt = self._load_personality()

        print("[INIT] Loading modules...")
        self.brain = Brain(system_prompt=self.system_prompt)
        self.actions = ActionEngine()
        self.memory = Memory()
        self.tts = None
        self.stt = None
        self.wake_word = None
        self.creator_name = None

        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _load_personality(self):
        pfile = BASE_DIR / "personality.txt"
        if pfile.exists():
            return pfile.read_text().strip()
        return "You are Vikram, a helpful AI assistant."

    def setup(self):
        print("[SETUP] First-time setup")
        name = input(f"Enter your name (default: Boss): ").strip()
        self.creator_name = name if name else "Boss"

        self.system_prompt = self._load_personality() + f"\n\nYour creator's name is {self.creator_name}."
        self.brain = Brain(system_prompt=self.system_prompt)

        voice_files = list((BASE_DIR / "voice").glob("*.wav")) + list((BASE_DIR / "voice").glob("*.mp3"))
        use_clone = "n"
        if voice_files:
            print(f"[SETUP] Voice sample detected: {voice_files[0].name}")
            use_clone = input("Use voice cloning? (y/n, default: y): ").strip().lower() or "y"
        else:
            print("[SETUP] No voice sample found.")
            record_now = input("Record your voice now (30s)? (y/n, default: n): ").strip().lower()
            if record_now == "y":
                self._record_voice()
                use_clone = "y"

        self.tts = TextToSpeech(use_cloned_voice=(use_clone == "y"))

        use_ww = input("Enable wake word detection? (y/n, default: y): ").strip().lower()
        if use_ww == "n":
            print("[INFO] Wake word disabled. Type 'vikram' to activate.")
        print("[SETUP] Complete!\n")

    def _record_voice(self):
        try:
            import sounddevice as sd
            import scipy.io.wavfile as wav
            import numpy as np
            print("\n[RECORD] Speak naturally for 30 seconds...")
            print("         Say: 'Hello, I am your creator.'")
            for i in range(3, 0, -1):
                print(f"         Starting in {i}...")
                __import__("time").sleep(1)
            fs = 16000
            audio = sd.rec(int(30 * fs), samplerate=fs, channels=1)
            sd.wait()
            out = BASE_DIR / "voice" / "my_voice.wav"
            wav.write(str(out), fs, np.int16(audio * 32767))
            print(f"[RECORD] Saved: {out}")
        except Exception as e:
            print(f"[RECORD] Failed: {e}")
            print("[RECORD] Record manually with record_voice.py")

    def on_wake_word(self):
        print("\n[VIKRAM] Yes?")
        self.tts.say("Yes?")
        self.process_command()

    def listen(self, duration=5):
        if not self.stt:
            self.stt = SpeechToText(model_size="tiny")
        print("[LISTEN] Listening...")
        text = self.stt.transcribe(duration=duration)
        print(f"[YOU] {text}")
        return text

    def process_command(self, text=None):
        if not text:
            text = self.listen()

        if not text:
            self.tts.say("I didn't catch that")
            return

        if text.lower() in ["exit", "quit", "bye", "goodbye"]:
            self.tts.say("Goodbye")
            self.running = False
            return

        if text.lower() in ["cancel shutdown", "abort shutdown"]:
            import subprocess
            subprocess.run(["shutdown", "/a"])
            self.tts.say("Shutdown cancelled")
            return

        action_result = self.actions.execute(text)
        if action_result:
            print(f"[ACTION] {action_result}")
            self.tts.say(action_result)
            return

        if "remember" in text.lower() and len(text) > 12:
            content = text.lower().replace("remember", "", 1).strip()
            result = self.memory.remember(content)
            self.tts.say(result)
            return

        if "recall" in text.lower() or "what do you remember" in text.lower() or "search memory" in text.lower():
            query = text.lower().replace("recall", "").replace("what do you remember", "").replace("search memory", "").strip()
            result = self.memory.recall(query if query else "everything")
            self.tts.say(result)
            return

        if "remind me" in text.lower() or "set a reminder" in text.lower():
            import re
            mins_match = re.search(r"in (\d+) (minute|min)s?", text)
            mins = int(mins_match.group(1)) if mins_match else 5
            reminder_text = text.lower().replace("remind me to", "").replace("set a reminder to", "").replace("in " + str(mins) + " minutes", "").replace("in " + str(mins) + " min", "").strip()
            result = self.memory.set_reminder(reminder_text, mins)
            self.tts.say(result)
            return

        if "note" in text.lower() and "save" in text.lower():
            parts = text.split("save a note", 1)
            if len(parts) > 1:
                content = parts[1].strip()
                title = content.split(",")[0] if "," in content else content[:30]
                result = self.memory.save_note(title, content)
                self.tts.say(result)
                return

        if "my notes" in text.lower() or "show notes" in text.lower():
            result = self.memory.list_notes()
            self.tts.say(f"Your recent notes: {result}")
            return

        print(f"[BRAIN] Thinking...")
        context = None
        recall = self.memory.recall(text, k=3)
        if recall != "Nothing found in memory.":
            context = f"Relevant memories:\n{recall}"

        reply = self.brain.think(text, context=context)
        print(f"[{VIKRAM_NAME}] {reply}")
        self.tts.say(reply)

    def reminder_checker(self):
        while self.running:
            try:
                due = self.memory.check_reminders()
                if due:
                    for r in due:
                        print(f"[REMINDER] {r}")
                        self.tts.say(f"Reminder: {r}")
            except:
                pass
            time.sleep(30)

    def console_mode(self):
        print(f"\n[INFO] Console mode. Type 'exit' to quit.\n")
        while self.running:
            try:
                user_input = input(">> ").strip()
                if user_input:
                    self.process_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                self.running = False
                break

    def voice_mode(self):
        print("[INFO] Voice mode active.")

        wake_keyword = VIKRAM_NAME.lower()
        print(f"  Speak to activate, or type 'vikram' in console\n")

        try:
            self.wake_word = WakeWordDetector(keyword=wake_keyword, callback=self.on_wake_word)
            self.wake_word.start()
        except Exception as e:
            print(f"[WARN] Wake word not available: {e}")
            print("[INFO] Falling back to push-to-talk (press Enter)")
            self.voice_mode_ptt()
            return

        reminder_thread = threading.Thread(target=self.reminder_checker, daemon=True)
        reminder_thread.start()

        try:
            while self.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            self.wake_word.stop()

    def voice_mode_ptt(self):
        reminder_thread = threading.Thread(target=self.reminder_checker, daemon=True)
        reminder_thread.start()

        while self.running:
            try:
                cmd = input("Press Enter to talk (type 'exit' to quit): ").strip().lower()
                if cmd == "exit":
                    self.running = False
                    break
                self.process_command()
            except KeyboardInterrupt:
                self.running = False
                break

    def start(self):
        self.setup()

        mode = input("Choose mode - (v)oice or (c)onsole: ").strip().lower()
        if mode == "c":
            self.console_mode()
        else:
            self.voice_mode()


if __name__ == "__main__":
    assistant = VikramAssistant()
    assistant.start()
