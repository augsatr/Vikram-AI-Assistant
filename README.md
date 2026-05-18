<div align="center">
  <h1>🧠 Vikram AI Assistant</h1>
  <p><em>A JARVIS-like intelligent voice assistant — 100% local, zero cloud dependencies</em></p>

  <p>
    <img src="https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white" alt="Python 3.12">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
    <img src="https://img.shields.io/badge/ollama-v0.24+-orange?logo=ollama" alt="Ollama">
    <img src="https://img.shields.io/badge/whisper-tiny-ff69b4" alt="Whisper tiny">
    <img src="https://img.shields.io/badge/platform-windows-lightgrey" alt="Windows">
    <img src="https://img.shields.io/badge/status-beta-yellow" alt="Beta">
  </p>

  <br>
</div>

Vikram is a desktop AI assistant that listens, thinks, speaks, and controls your PC. Inspired by JARVIS from Iron Man, it runs entirely offline using open-source models — no internet required after setup.
<img src="https://giffiles.alphacoders.com/212/212508.gif" alt="">
---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [System Requirements](#-system-requirements)
- [Quick Start](#-quick-start)
- [Detailed Installation](#-detailed-installation)
- [Voice Modes](#-voice-modes)
- [Voice Cloning (Madara Uchiha)](#-voice-cloning-madara-uchiha)
- [Commands & Actions](#-commands--actions)
- [Memory System](#-memory-system)
- [Architecture](#-architecture)
- [Configuration Reference](#-configuration-reference)
- [Dependencies](#-dependencies)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Developer](#-developer)

---

## ✨ Features

| # | Capability | Engine | Details |
|---|-----------|--------|---------|
| 1 | 🎤 **Wake Word** | OpenWakeWord | Say *"hey jarvis"* — no API key needed |
| 2 | 🗣️ **Speech-to-Text** | OpenAI Whisper (tiny) | 72MB model, runs on CPU, ~5s for 5s audio |
| 3 | 🧠 **AI Brain** | Ollama + TinyLlama / Qwen 2.5 | Context-aware reasoning with personality |
| 4 | 🔊 **Voice Output** | Edge-TTS / XTTS v2 | Neural voices (fast) or clone any voice |
| 5 | 💾 **Memory** | FAISS + all-MiniLM-L6-v2 | Semantic search across chat history |
| 6 | ⏰ **Reminders** | In-memory scheduler | *"Remind me in 10 minutes to check the oven"* |
| 7 | 🖥️ **System Control** | PyAutoGUI + subprocess | Launch apps, volume, shutdown, cancel shutdown |
| 8 | 📝 **Notes** | FAISS vector storage | *"Remember that my wifi password is vikram123"* |
| 9 | 🎭 **Personality** | Custom system prompt | JARVIS-style — polite, witty, helpful |
| 10 | 🔌 **Extensible** | Modular design | Add new commands in `modules/actions.py` |

---

## 🖥️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| **RAM** | 4 GB | 8 GB |
| **Storage** | 2 GB free | 5 GB free (for LLM models) |
| **OS** | Windows 10 | Windows 11 |
| **Microphone** | Any built-in or USB mic | Noise-cancelling headset |
| **Speakers** | Any output device | Any output device |
| **Internet** | Required only for first-time setup | Not required during use |

**Note:** Vikram runs entirely on CPU (no GPU needed). Inference is slower but functional.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/augsatr/Vikram-AI-Assistant.git
cd Vikram-AI-Assistant

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Ollama (download from https://ollama.com)
#    Then pull a model:
ollama pull tinyllama

# 4. Start Ollama server
ollama serve

# 5. Launch Vikram
vikram.bat
```

---

## 📦 Detailed Installation

### Step 1: Python 3.12

Download from [python.org](https://python.org) or Microsoft Store. Verify:

```bash
python --version
# Python 3.12.x
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including PyTorch (CPU), Whisper, FAISS, sentence-transformers, TTS, pvporcupine, edge-tts, and more.

### Step 3: Ollama Setup

1. Download Ollama from [ollama.com](https://ollama.com)
2. Install and run the installer
3. Pull a compatible model:

```bash
# Recommended for 8GB RAM:
ollama pull tinyllama

# Better quality (4.7GB, requires patience):
ollama pull qwen2.5
```

4. Start the server:

```bash
ollama serve
```

Vikram auto-detects available models and falls back if `qwen2.5` isn't found.

### Step 4: Configuration (Optional)

Copy `.env.example` to `.env` and customize:

```bash
copy .env.example .env
```

### Step 5: Launch

```bash
vikram.bat
```

---

## 🎤 Voice Modes

### Console Mode (`c`)

Type commands directly. Best for development and testing.

```
>> hello
[VIKRAM] Hello! How can I assist you today?
>> what's the weather?
[VIKRAM] I don't have internet access, but I can help with system tasks.
>> open chrome
[ACTION] Opening Chrome...
```

### Voice Mode (`v`)

Hands-free interaction with wake word activation.

1. Say **"hey jarvis"** to activate listening
2. Vikram beeps and starts recording (5 seconds)
3. Your speech is transcribed and processed
4. Vikram responds with voice output

> **Note:** Voice mode requires a working microphone. If microphone levels are too low, Vikram automatically falls back to push-to-talk (press Enter to talk).

### Push-to-Talk

If wake word isn't available, Vikram enters push-to-talk mode automatically:

```
Press Enter to talk (type 'exit' to quit): [press Enter]
[Listening...] "What time is it?"
[VIKRAM] It's 3:45 PM.
```

---

## 🎭 Voice Cloning (Madara Uchiha)

Vikram can clone any voice from a short audio sample. The setup uses **Madara Uchiha's voice** from Naruto for that iconic deep tone.

### How to use:

1. **Place** a `.wav` file (10-60 seconds, 16kHz mono) in the `voice/` folder
2. **Run** `vikram.bat` and enable voice cloning during setup
3. **XTTS v2** generates all responses in the cloned voice

### Performance:

| Mode | Load Time | Generation (per response) | Quality |
|------|-----------|--------------------------|---------|
| **Edge-TTS** | Instant | ~2 seconds | ★★★★☆ Neural |
| **XTTS v2** | ~80 seconds (first time) | ~27 seconds | ★★★★★ Cloned voice |

> Edge-TTS is the default for responsiveness. Voice cloning is available as an optional enhancement.

### Create your own:

```bash
# Record 30 seconds of speech:
python record_voice.py
# Then select the .wav file during setup
```

---

## 🎮 Commands & Actions

| Category | Phrase | Action |
|----------|--------|--------|
| **Exit** | *"exit"*, *"quit"*, *"bye"*, *"goodbye"* | Terminates Vikram |
| **Memory** | *"remember [something]"* | Saves to long-term memory |
| **Memory** | *"recall [topic]"* | Searches memory for relevant info |
| **Memory** | *"what do you remember about [topic]"* | Semantic memory search |
| **Reminders** | *"remind me to [task] in [N] minutes"* | Sets a timer reminder |
| **Notes** | *"save a note [title], [content]"* | Stores a note |
| **Notes** | *"show my notes"* | Lists recent notes |
| **System** | *"open [app name]"* | Launches application |
| **System** | *"volume up/down"* | Adjusts system volume |
| **System** | *"shutdown"* | Initiates shutdown (30s delay) |
| **System** | *"cancel shutdown"* | Aborts pending shutdown |
| **Chat** | *anything else* | General conversation via LLM |

---

## 💾 Memory System

Vikram uses a **FAISS (Facebook AI Similarity Search)** vector database for persistent memory.

### How it works:

1. **Embeddings**: All text is converted to 384-dimensional vectors using `all-MiniLM-L6-v2`
2. **Storage**: Vectors are stored in `data/memory.faiss` with metadata in `data/memory.json`
3. **Search**: When you ask a question, Vikram searches the top-3 most semantically similar memories
4. **Context**: Relevant memories are injected into the LLM prompt as context

### Example:

```
>> remember that my favorite color is midnight blue
[VIKRAM] I'll remember that.

>> recall my favorite color
[VIKRAM] Your favorite color is midnight blue.
```

### Reminders:

```
>> remind me to take a break in 5 minutes
[VIKRAM] I'll remind you in 5 minutes.
... (5 minutes later)
[REMINDER] Take a break!
```

---

## 🧠 Architecture

```
vikram.py                         # Entry point — user input → response loop
│
├── config.py                     # Auto-detect model, load .env settings
├── personality.txt               # JARVIS-like system prompt
│
├── modules/
│   ├── wake_word.py              # OpenWakeWord — voice activity detection
│   ├── stt.py                    # Whisper — audio → text transcription
│   ├── brain.py                  # Ollama — text → intelligent response
│   ├── tts.py                    # Edge-TTS / XTTS v2 — text → speech
│   ├── actions.py                # Keyword matching → system commands
│   └── memory.py                 # FAISS + sentence-transformers → memory
│
├── voice/                        # Voice cloning samples (.wav)
├── data/                         # FAISS index, notes, reminders (auto-created)
│
├── vikram.bat                    # One-click Windows launcher
├── setup.bat                     # First-time dependency installer
├── requirements.txt              # Python package manifest
├── .env.example                  # Configuration template
└── .gitignore                    # Python + binaries + data exclusion
```

### Data Flow:

```
User speaks → Microphone → [Wake Word] → Whisper STT → Ollama LLM
                                                              ↓
User hears ← Speakers ← [TTS Engine] ← Vikram response ←─ Actions/Memory
```

---

## ⚙️ Configuration Reference

All settings can be configured via `.env` file or environment variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API server address |
| `OLLAMA_MODEL` | `qwen2.5` | LLM model (auto-falls back to tinyllama) |
| `VIKRAM_NAME` | `Vikram` | How the assistant refers to itself |
| `AUDIO_DEVICE_INDEX` | `-1` | Microphone index (-1 = system default) |
| `AUDIO_SAMPLE_RATE` | `16000` | Audio sample rate for STT |
| `PORCUPINE_API_KEY` | `""` | Picovoice API key (optional) |
| `WAKE_WORD_SENSITIVITY` | `0.5` | Wake word detection threshold |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `torch` | 2.x (CPU) | PyTorch runtime for Whisper/TTS |
| `whisper` | 20240930 | OpenAI speech recognition |
| `ollama` | 0.4+ | Python client for Ollama API |
| `faiss-cpu` | 1.9+ | Facebook vector similarity search |
| `sentence-transformers` | 3.x | Text-to-embedding conversion |
| `TTS` | 0.27+ | Coqui TTS (XTTS v2 voice cloning) |
| `edge-tts` | 6.x | Microsoft Edge neural TTS |
| `pvporcupine` | 3.x | Porcupine wake word engine |
| `openwakeword` | 0.6+ | Open-source wake word detection |
| `sounddevice` | 0.5+ | PortAudio audio capture/playback |
| `pyautogui` | 0.9+ | GUI automation for system control |
| `soundfile` | 0.12+ | WAV file I/O |
| `python-dotenv` | 1.x | .env file loading |

---

## 🔧 Troubleshooting

### "No module named X" error

```bash
pip install -r requirements.txt
```

### Ollama connection refused

1. Ensure Ollama is running: `ollama serve`
2. Check the host in `.env`: `OLLAMA_HOST=http://localhost:11434`
3. Try: `curl http://localhost:11434/api/tags`

### Microphone not working

- Check Windows privacy settings: Settings → Privacy & security → Microphone
- Ensure microphone is not muted
- Try a different microphone device
- Use **console mode** as a fallback: type `c` at startup

### Voice output not audible

- Check speaker volume
- Ensure audio output device is connected
- `winsound` uses the system default playback device

### TTS taking too long

- XTTS v2 takes ~30s per response on CPU — this is normal
- Switch to Edge-TTS by disabling voice cloning during setup
- Edge-TTS responses arrive in ~2 seconds

### Wake word not detecting

- OpenWakeWord model is sensitive to pronunciation
- Try saying "hey jarvis" clearly
- Reduce ambient noise
- Fall back to push-to-talk (automatic)

---

## 🗺️ Roadmap

- [x] Wake word detection
- [x] Offline speech recognition
- [x] Local LLM integration
- [x] Voice cloning (XTTS v2)
- [x] FAISS memory system
- [x] System actions (apps, volume, shutdown)
- [x] Notes and reminders
- [ ] Web search integration
- [ ] Spotify/YouTube music control
- [ ] Email and calendar integration
- [ ] Mobile companion app
- [ ] Custom wake word training
- [ ] Multi-language support

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Developer

**Sohan** — [@augsatr](https://github.com/augsatr)

> *"A true shinobi never gives up, and neither does Vikram."*
