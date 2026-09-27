# 🤖 JARVIS — Day 2: Voice Input + Voice Output

This is the small, beginner-friendly Day 2 version of the JARVIS project.

It demonstrates:

- 🎙️ Microphone input
- 👂 Gemini Live listening
- 🧠 AI understanding
- 🔊 Gemini-generated voice output

The code is intentionally separate from the full JARVIS project, so beginners can understand the voice pipeline without downloading the entire application.

## 1. Requirements

- Windows / macOS / Linux
- Python 3.10+
- A working microphone
- Speakers or headphones
- A Gemini API key

## 2. Install the libraries

Open Terminal / PowerShell inside this folder and run:

```bash
pip install -r requirements.txt
```

## 3. Add your Gemini API key

Do NOT put your API key directly into `jarvis_voice.py`.

### Windows PowerShell

Run:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your real Gemini API key.

This environment variable lasts for the current PowerShell window.

## 4. Run JARVIS

```bash
python jarvis_voice.py
```

You should see:

```text
[JARVIS] Connected. Listening...
```

Now speak into your microphone.

JARVIS sends the microphone's PCM audio to Gemini Live and receives generated audio back.

## 5. Stop JARVIS

Press:

```text
Ctrl + C
```

## How it works

```text
Microphone
    ↓
16 kHz PCM audio
    ↓
Gemini Live
    ↓
AI understands speech
    ↓
Generated audio response
    ↓
Speaker / Headphones
```

## Important

This is a learning/demo package for Day 2. It is NOT the complete 2,000+ line JARVIS application.

The full project can later add:

- Memory
- PC control
- Browser control
- Vision
- Wake word
- Tools
- UI
- More advanced voice behavior

## Troubleshooting

### Microphone error

Make sure Windows has microphone permission enabled:

Settings → Privacy & security → Microphone

Also check that the correct microphone is selected.

### No audio output

Check your Windows output device and make sure your speakers/headphones are working.

### API key error

If you see:

```text
GEMINI_API_KEY is not set
```

set the environment variable again in the same PowerShell window:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Then run:

```bash
python jarvis_voice.py
```

## Day 2

Built as part of the:

**10 DAYS → MY OWN JARVIS 🤖**

Follow the build for Day 3.
