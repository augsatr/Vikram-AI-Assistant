<div align="center">
  <h1>🧠 Vikram AI Assistant</h1>
  <p><em>A JARVIS-like intelligent voice assistant — 100% local, zero cloud dependencies</em></p>

  <p>
    <img src="https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
    <img src="https://img.shields.io/badge/ollama-v0.24+-orange?logo=ollama" alt="Ollama">
    <img src="https://img.shields.io/badge/whisper-tiny-ff69b4" alt="Whisper tiny">
    <img src="https://img.shields.io/badge/platform-windows-lightgrey" alt="Windows">
  </p>
</div>

---

## ✨ Features

| Capability | Engine | Description |
|-----------|--------|-------------|
| 🎤 **Wake Word** | OpenWakeWord | Say *"hey jarvis"* to activate |
| 🗣️ **Speech-to-Text** | OpenAI Whisper (tiny) | Offline transcription, CPU-optimized |
| 🧠 **AI Brain** | Ollama + TinyLlama / Qwen 2.5 | Local LLM reasoning |
| 🔊 **Voice Output** | Edge-TTS / XTTS v2 | Neural voices or custom voice cloning |
| 💾 **Memory** | FAISS + sentence-transformers | Semantic search across conversations |
| ⏰ **Reminders** | In-memory scheduler | Voice-triggered timer alerts |
| 🖥️ **System Control** | PyAutoGUI | Launch apps, volume, shutdown |
| 📝 **Notes** | Vector storage | Save, search, and recall notes |

---

## 🚀 Quick Start

### Prerequisites

- **Windows** (10/11)
- **Python 3.12+**
- **Ollama** ([download](https://ollama.com))

### 1. Clone & install

```bash
git clone https://github.com/augsatr/Vikram-AI-Assistant.git
cd Vikram-AI-Assistant
pip install -r requirements.txt
```

### 2. Pull an LLM

```bash
ollama pull tinyllama
ollama serve
```

### 3. Launch Vikram

```bash
vikram.bat
```

Choose **console mode** (`c`) to type commands, or **voice mode** (`v`) for wake-word activated interaction.

---

## 🎤 Voice Cloning

Vikram can clone any voice from a short audio sample — including **Madara Uchiha's** voice:

1. Place a `.wav` file in `voice/`
2. During setup, enable **voice cloning**
3. XTTS v2 generates responses in the cloned voice

> **Note:** XTTS v2 runs on CPU (~30s per response). For daily use, Edge-TTS neural voices are recommended for responsiveness.

---

## 🧠 Architecture

```
vikram.py              # Entry point — orchestrates all modules
├── modules/
│   ├── wake_word.py   # OpenWakeWord voice activity detection
│   ├── stt.py         # Whisper speech-to-text
│   ├── brain.py       # Ollama LLM interaction
│   ├── tts.py         # Edge-TTS / XTTS v2 speech synthesis
│   ├── actions.py     # PyAutoGUI system control
│   └── memory.py      # FAISS vector DB + reminders
├── config.py           # Auto-detection of available models
├── personality.txt     # JARVIS-style system prompt
├── voice/              # Voice cloning samples
└── data/               # FAISS index + notes storage
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `qwen2.5` (auto-fallback) | LLM model name |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `VIKRAM_NAME` | `Vikram` | Assistant identity name |
| `AUDIO_DEVICE_INDEX` | `-1` (system default) | Microphone device index |
| `WAKE_WORD_SENSITIVITY` | `0.5` | Detection sensitivity |

Copy `.env.example` to `.env` and adjust as needed.

---

## 🛠 Tech Stack

| Technology | Role |
|-----------|------|
| [Python 3.12](https://python.org) | Core runtime |
| [Ollama](https://ollama.com) | Local LLM orchestration |
| [Whisper](https://github.com/openai/whisper) | Offline speech recognition |
| [XTTS v2](https://github.com/coqui-ai/TTS) | Voice cloning synthesis |
| [Edge-TTS](https://github.com/rany2/edge-tts) | Cloud neural TTS |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search |
| [Sentence-Transformers](https://www.sbert.net) | Text embeddings |
| [PyAutoGUI](https://github.com/asweigart/pyautogui) | Desktop automation |

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Developer

**Sohan** — [@augsatr](https://github.com/augsatr)

> *"A true shinobi never gives up, and neither does Vikram."*
