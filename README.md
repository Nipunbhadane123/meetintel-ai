# MeetIntel AI - AI-Powered Meeting Intelligence Platform

Welcome to **MeetIntel AI**, an advanced AI application that turns your meeting recordings into structured, searchable, and actionable insights.

This project was built for the Infosys Springboard internship.

## 1. What this project does

MeetIntel AI takes an audio or video recording of a meeting and automatically transforms it into:
- A clean-verbatim, speaker-labelled transcript (using Whisper and Pyannote)
- An AI-generated Executive Summary
- Key Discussion Points & Topics
- Extracted Decisions and Action Items
- A Meeting Follow-up Plan
- Professional Minutes of Meeting (MoM)

You can understand exactly what happened in a 1-hour meeting in 2 minutes, without needing to listen to the recording!

---

## 2. Features
- **Local AI Transcription**: Uses `faster-whisper` for fast, private transcription.
- **Speaker Diarization**: Uses `pyannote.audio` to figure out *who* said *what*.
- **AI Intelligence Layer**: Uses Google Gemini (or OpenAI) to extract insights into structured JSON.
- **Mac Optimized**: Works flawlessly on Apple Silicon (M1/M2/M3/M4) MacBooks.
- **Export**: Download your MoM in PDF/DOCX format.

---

## 3. System Requirements
- **OS**: macOS (M-Series Apple Silicon highly recommended)
- **Memory**: Minimum 8GB RAM (16GB recommended for `large-v3` Whisper models)
- **Disk Space**: At least 5GB free space (for models and virtual environments)
- **External Tools**: `ffmpeg` (required for media processing)
- **Accounts**: Hugging Face (for Pyannote), Google Gemini (for AI Insights)

---

## 4. Beginner-Friendly MacBook Setup

Follow these instructions exactly if you are on an Apple Silicon Mac.

### Check Existing Installation
First, open **Terminal** (`Cmd + Space`, type "Terminal", press Enter). Check your architecture:
```bash
uname -m
```
*Expected output: `arm64` (This means you are on Apple Silicon).*

Check Python and git:
```bash
python3 --version
git --version
```
*If it says "command not found", a pop-up might ask you to install Command Line Tools. Click Install.*

---

### 5. FFmpeg Setup (Critical!)
This app needs `ffmpeg` to extract audio from video files.
If you don't have Homebrew installed, install it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then install `ffmpeg`:
```bash
brew install ffmpeg
```
Verify it:
```bash
ffmpeg -version
```

---

### 6. Project Installation

Clone the repository and move into the folder:
```bash
git clone https://github.com/yourusername/meeting-intelligence.git
cd meeting-intelligence
```
*(If you downloaded a ZIP, extract it, open Terminal, type `cd `, drag the extracted folder into the terminal, and press Enter).*

---

### 7. Virtual Environment & Dependencies
Create an isolated Python environment:
```bash
python3 -m venv .venv
```
Activate it (You must do this every time you open a new terminal!):
```bash
source .venv/bin/activate
```
*(Your terminal prompt should now start with `(.venv)`).*

Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 8. API Keys Setup
1. **Hugging Face**: Go to [huggingface.co](https://huggingface.co), create an account, go to Settings -> Access Tokens, and create a Read token. **You must also go to `pyannote/speaker-diarization-community-1` on Hugging Face and accept the user conditions.**
2. **Google Gemini**: Go to [Google AI Studio](https://aistudio.google.com/), get an API key.

Copy the example file:
```bash
cp .env.example .env
```
Open `.env` in a text editor and paste your keys:
```env
HUGGINGFACE_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
```

---

### 9. Health Check
Run the diagnostic script to ensure everything is perfect:
```bash
python scripts/health_check.py
```
If the status is **READY**, you are good to go!

---

### 10. Running the Application
Ensure your virtual environment is active, then run:
```bash
streamlit run app.py
```
Your browser will open to `http://localhost:8501`. 

---

### 11. Troubleshooting on MacBook

- **`ffmpeg: command not found`**: Ensure Homebrew installed it correctly. Try running `brew link ffmpeg`.
- **`bad CPU type in executable`**: You are trying to run an Intel application on an Apple Silicon Mac. Ensure you installed the native Python 3 for ARM64 from python.org or Homebrew.
- **Port already in use**: Streamlit might complain port 8501 is busy. Run `streamlit run app.py --server.port 8502`.

---

## 12. Project Architecture & Milestone 1 Mapping

- **Task 1 (Whisper)** -> `transcription/whisper_engine.py`
- **Task 2 (File Validation)** -> `audio/validator.py`
- **Task 3 (Transcript Validation)** -> `validation/transcript_validator.py`
- **Task 4 (Streamlit UI)** -> `app.py`, `ui/`
- **Task 5 (Accuracy/WER)** -> `validation/accuracy.py`
- **AI Analytics** -> `ai/`

---
*Built with ❤️ for Infosys Springboard.*
