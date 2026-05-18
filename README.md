# 🧠 Vikram AI Assistant

> *A JARVIS-like intelligent voice assistant — runs 100% locally, no cloud required.*

Vikram is a desktop AI assistant that listens, thinks, speaks, and controls your PC. Built with offline-first philosophy — everything runs on your machine using open-source models.
<img src="https://giffiles.alphacoders.com/212/212508.gif" alt="">

---

## ✨ Features

| Capability | How it works |
|-----------|--------------|
| **Wake word** | OpenWakeWord — say "hey jarvis" to activate |
| **Speech recognition** | OpenAI Whisper (tiny) — offline transcription |
| **AI brain** | Ollama + TinyLlama / Qwen 2.5 7B — local LLM |
| **Voice output** | Edge-TTS (neural) or XTTS v2 (voice cloning) |
| **Memory** | FAISS vector database + sentence-transformers |
| **Reminders** | In-memory timer with TTS alerts |
| **System actions** | Open apps, control volume, shutdown PC |
| **Notes** | Save, search, and recall notes |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install & start Ollama

Download from [ollama.com](https://ollama.com), then:

```bash
ollama pull tinyllama
ollama serve
```

### 3. Run Vikram

```bash
vikram.bat
```

Choose **console mode** (`c`) to type commands, or **voice mode** (`v`) for hands-free.

---

## 🎤 Voice Cloning (Madara Uchiha)

Vikram can clone any voice from a short audio sample:

1. Place a `.wav` file in the `voice/` folder
2. During setup, choose **voice cloning**
3. XTTS v2 generates speech in the cloned voice

> **Note:** XTTS v2 runs on CPU and takes ~30s per response. For daily use, Edge-TTS (instant) is recommended.

---

## 🧠 Architecture

```
vikram.py          →  Main entry point
modules/
├── wake_word.py   →  Voice activity detection
├── stt.py         →  Whisper speech-to-text
├── brain.py       →  Ollama LLM interaction
├── tts.py         →  Text-to-speech (Edge-TTS / XTTS v2)
├── actions.py     →  System control
└── memory.py      →  FAISS vector memory + reminders
config.py          →  Model auto-detection & settings
personality.txt    →  JARVIS-like system prompt
```

---

## ⚙️ Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_MODEL` | `qwen2.5` (auto-fallsback) | LLM model name |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server |
| `VIKRAM_NAME` | `Vikram` | Assistant name |
| `AUDIO_DEVICE_INDEX` | `-1` (default mic) | Microphone index |

Set these in `.env` or `config.py`.

---

## 🛠 Tech Stack

- **Python 3.12** — Core language
- **Ollama** — Local LLM server
- **Whisper** — Offline speech recognition
- **XTTS v2 / Edge-TTS** — Voice synthesis
- **FAISS** — Vector similarity search
- **Sentence-Transformers** — Text embeddings
- **PyAutoGUI** — System control

---

## 📦 Project Structure

```
Vikram/
├── vikram.py              # Main assistant
├── modules/
│   ├── wake_word.py       # OpenWakeWord detection
│   ├── stt.py             # Whisper STT
│   ├── brain.py           # Ollama LLM
│   ├── tts.py             # TTS output
│   ├── actions.py         # System actions
│   └── memory.py          # FAISS memory
├── config.py              # Configuration
├── personality.txt        # System prompt
├── voice/                 # Voice samples
├── data/                  # Memory storage
├── requirements.txt       # Dependencies
├── vikram.bat             # Launcher
└── setup.bat              # One-time setup
```

---

## 📄 License

MIT

---

## 👨‍💻 Developer

Created by [augsatr](https://github.com/augsatr)

*"A true shinobi never gives up, and neither does Vikram."*
