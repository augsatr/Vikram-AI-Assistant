import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from datetime import datetime
from config import MEMORY_FILE, REMINDERS_FILE, DATA_DIR

class Memory:
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []
        self._load_index()

    def _load_index(self):
        if MEMORY_FILE.exists():
            try:
                self.index = faiss.read_index(str(MEMORY_FILE))
                meta = MEMORY_FILE.with_suffix(".json")
                if meta.exists():
                    self.texts = json.loads(meta.read_text())
            except:
                print("[MEMORY] Could not load existing index, starting fresh")

    def _save_index(self):
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(MEMORY_FILE))
        meta = MEMORY_FILE.with_suffix(".json")
        meta.write_text(json.dumps(self.texts))

    def remember(self, text):
        vec = self.encoder.encode([text]).astype(np.float32)
        self.index.add(vec)
        self.texts.append(text)
        self._save_index()
        return f"Remembered: {text[:50]}..."

    def recall(self, query, k=3):
        if self.index.ntotal == 0:
            return "I have no memories stored yet."
        vec = self.encoder.encode([query]).astype(np.float32)
        distances, indices = self.index.search(vec, min(k, self.index.ntotal))
        results = [self.texts[i] for i in indices[0] if i < len(self.texts)]
        if not results:
            return "Nothing found in memory."
        return "\n".join(results)

    def save_note(self, title, content):
        notes_file = DATA_DIR / "notes.json"
        notes = []
        if notes_file.exists():
            notes = json.loads(notes_file.read_text())
        notes.append({"title": title, "content": content, "date": datetime.now().isoformat()})
        notes_file.write_text(json.dumps(notes, indent=2))
        return f"Note '{title}' saved."

    def list_notes(self):
        notes_file = DATA_DIR / "notes.json"
        if not notes_file.exists():
            return "No notes saved."
        notes = json.loads(notes_file.read_text())
        return "\n".join(f"- {n['title']}: {n['content'][:60]}..." for n in notes[-5:])

    def set_reminder(self, text, minutes=5):
        reminders = []
        if REMINDERS_FILE.exists():
            reminders = json.loads(REMINDERS_FILE.read_text())
        reminders.append({"text": text, "time": (datetime.now().timestamp() + minutes * 60), "minutes": minutes})
        REMINDERS_FILE.write_text(json.dumps(reminders))
        return f"Reminder set for {minutes} minutes: {text}"

    def check_reminders(self):
        if not REMINDERS_FILE.exists():
            return None
        reminders = json.loads(REMINDERS_FILE.read_text())
        now = datetime.now().timestamp()
        due = [r for r in reminders if r["time"] <= now]
        if due:
            reminders = [r for r in reminders if r["time"] > now]
            REMINDERS_FILE.write_text(json.dumps(reminders))
            return [r["text"] for r in due]
        return None
