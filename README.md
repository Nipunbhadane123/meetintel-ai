# MeetIntel AI

## AI-Powered Meeting Intelligence Platform

MeetIntel AI is an advanced application that transforms meeting recordings into structured, searchable, and actionable knowledge. Instead of just generating a raw transcript, the system uses AI to understand the conversation, extract decisions and action items, identify speakers, and store the meeting in a persistent vector knowledge base. This allows users to search across all their historical meetings or ask natural-language questions to instantly retrieve information that would otherwise be lost.

---

## 2. Project Overview

Meetings contain critical decisions, responsibilities, and deadlines. However, manually reviewing hour-long audio recordings or reading unstructured transcripts is extremely time-consuming. When a decision gets buried an hour into a meeting, it often gets lost completely.

MeetIntel AI addresses this problem by combining:
- Local speech-to-text processing
- Speaker diarization
- LLM-based structured information extraction
- Relational meeting storage
- Vector embeddings and semantic search
- Retrieval-Augmented Generation (RAG)
- Streamlit-based UI and FastAPI backend
- User-level authentication and data isolation

The goal is to move from **recording a meeting** to **understanding and querying a meeting**.

---

## 3. Why MeetIntel AI?

**Traditional Meeting Recording:**
- Stores raw audio/video.
- Extremely difficult to review or search.
- Critical information remains buried and inaccessible.

**Basic Transcription:**
- Produces a wall of text.
- Still requires manual human analysis.
- Decisions, deadlines, and action items are not structured.

**MeetIntel AI:**
- Generates high-accuracy transcriptions.
- Identifies who spoke when (Speaker Diarization).
- Automatically writes executive summaries.
- Extracts structured arrays of decisions, action items, participants, and deadlines.
- Builds a searchable vector knowledge base.
- Enables Semantic Search and RAG-based AI question answering.
- Generates downloadable PDF/CSV/DOCX reports.

---

## 4. Key Features

### Authentication & User Access
- Registration and login system
- Secure password hashing
- Session handling via Streamlit state
- User-specific meeting retrieval
- Strict user-level data isolation

### Meeting Processing
- Audio/video upload via the UI
- File validation and format checking
- FFmpeg audio preprocessing
- Local Speech-to-Text using Faster-Whisper
- Speaker diarization using Pyannote.audio
- Generation of a clean, speaker-labelled transcript

### AI Meeting Intelligence
- Executive summary generation
- Key discussion points extraction
- Structured decision extraction
- Action item mapping (task, assignee, status)
- Participant mapping (name, responsibilities)
- Deadline and priority tracking
- Strict Pydantic schema validation for AI outputs

### Knowledge Repository
- Persistent meeting storage in SQLite
- Transcript and metadata chunking
- Text embeddings using Sentence-Transformers
- Local vector database using ChromaDB
- Fast semantic search across historical meetings

### AI Assistant / RAG
- Natural-language questioning across the knowledge base
- Retrieval of relevant meeting chunks using semantic similarity
- Meeting-specific context bounding
- Source-aware answers to prevent hallucinations
- RAG (Retrieval-Augmented Generation) powered responses

### Reports
- Downloadable PDF export (Minutes of Meeting)
- CSV export for tabular data
- DOCX export

### AI Reliability
- Primary AI Provider: Google Gemini
- Fallback AI Provider: OpenAI
- Dynamic AI Provider Manager
- Built-in graceful failover if a provider hits a rate limit
- Automatic cooldowns for failing providers

### UI
- Responsive Streamlit interface
- Central dashboard for meeting overview
- Tab-based meeting detailed view
- Dedicated UI for RAG Knowledge Search
- Settings page for AI provider health checks
- Theme support (Light/Dark mode via CSS variables)

---

## 5. System Architecture

```text
User
  ↓
Streamlit UI
  ↓
Authentication / Session
  ↓
Meeting Upload
  ↓
File Validation
  ↓
FFmpeg (Audio Extraction)
  ↓
Faster-Whisper (Speech-to-Text)  <--->  Pyannote (Speaker Diarization)
  ↓
Speaker-Labeled Transcript
  ↓
AI Provider Manager (Graceful Failover)
  ↓
Gemini (Primary) / OpenAI (Fallback)
  ↓
Structured Meeting Insights (Pydantic Validated)
  ↓
SQLite / SQLAlchemy (Relational Metadata)
  ↓
Knowledge Repository (Chunking)
  ↓
Sentence-Transformers (Embeddings)
  ↓
ChromaDB (Vector Storage)
  ↓
Semantic Search / RAG
  ↓
FastAPI (API Layer)
  ↓
AI Assistant / Search / PDF/CSV Reports
```

---

## 6. Processing Pipeline

1. **Upload:** User authenticates and uploads a meeting recording.
2. **Preprocessing:** File validation runs, and FFmpeg converts/prepares the audio.
3. **Transcription:** Faster-Whisper generates an accurate transcript locally.
4. **Diarization:** Pyannote analyzes the audio to perform speaker diarization.
5. **Merging:** The raw text and speaker clusters are merged into a speaker-labeled transcript.
6. **Intelligence Extraction:** The `MeetingAnalyzer` sends the transcript to the AI provider.
7. **Generation:** The LLM generates structured meeting insights (JSON).
8. **Validation:** Pydantic schemas verify that the result correctly contains arrays of decisions, action items, etc.
9. **Persistence:** The structured data is persisted in the SQLite relational database.
10. **Indexing:** The transcript and insights are chunked into smaller segments.
11. **Embedding:** Embeddings are generated using local Sentence-Transformers.
12. **Vector Storage:** Chunks are stored in ChromaDB, tagged with the `user_id` and `meeting_id`.
13. **Retrieval:** The user performs a semantic search or asks a question in the UI.
14. **RAG:** The system retrieves the most relevant knowledge chunks from ChromaDB.
15. **Answering:** The AI assistant generates a grounded response using only the retrieved context, citing its sources.
16. **Export:** The user can export the processed meeting to a PDF, CSV, or DOCX report.

---

## 7. Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core application logic and orchestration. |
| **Streamlit** | Rapid, interactive Web UI for dashboards and AI chat. |
| **FastAPI** | High-performance REST API layer for system integrations. |
| **SQLite** | Lightweight relational persistence for users and meeting metadata. |
| **SQLAlchemy** | Database ORM for safe, structured database interactions. |
| **FFmpeg** | Reliable audio/video format preprocessing and extraction. |
| **Faster-Whisper** | Highly optimized, local speech-to-text processing. |
| **Pyannote.audio** | Advanced machine learning for speaker diarization. |
| **Gemini** | Primary LLM for deep meeting analysis and structured extraction. |
| **OpenAI** | Configured as an automatic fallback LLM provider. |
| **Sentence-Transformers** | Local generation of semantic text embeddings. |
| **ChromaDB** | Local, high-performance vector storage and similarity search. |
| **Pydantic** | Strict type checking and structured validation for AI outputs. |
| **FPDF** | Programmatic generation of PDF reports. |
| **Git/GitHub** | Version control. |

**Why these technologies?**
Python serves as the perfect glue between advanced AI/ML audio libraries (Whisper, Pyannote) and modern web frameworks (FastAPI, Streamlit). Faster-Whisper and ChromaDB were specifically chosen to run inference and vector searches locally, avoiding the latency and privacy concerns of cloud alternatives. Gemini and OpenAI provide the heavy reasoning required to extract structured intelligence from unstructured conversational transcripts.

---

## 8. AI Provider Architecture

To ensure the system remains reliable even if an external AI service goes down, MeetIntel AI implements a robust `AIProviderManager`:

```text
Primary Provider (Gemini)
      ↓
(If QuotaExhaustedError or TransientError)
      ↓
Mark Gemini as "Unhealthy" (Cooldown Period)
      ↓
Automatic Retry with Fallback Provider (OpenAI)
      ↓
Normalized Structured Output returned to Application
```

- **Abstraction:** Providers inherit from a base `AIProvider` class, ensuring normalized outputs regardless of the underlying LLM.
- **Graceful Failure:** If Gemini hits a rate limit, it is placed on a cooldown (e.g., 120 seconds). Requests are instantly routed to OpenAI without crashing the application or showing errors to the user.

---

## 9. RAG Architecture

MeetIntel AI implements Retrieval-Augmented Generation (RAG) to allow users to "chat" with their past meetings.

```text
User Question
      ↓
Query Embedding (Sentence-Transformers)
      ↓
Semantic Search (ChromaDB)
      ↓
Filter by User ID / Meeting ID
      ↓
Retrieve Top-K Relevant Meeting Chunks
      ↓
Context Construction
      ↓
LLM (Gemini/OpenAI)
      ↓
Grounded Answer with Sources
```

- **Semantic Retrieval:** Used for conceptual questions (e.g., *"Why did we choose Postgres over MySQL?"*). The system finds chunks of the transcript with similar meaning, rather than relying on exact keyword matches.
- **Source-Awareness:** The LLM is strictly prompted to only use the retrieved ChromaDB chunks. If the answer is not present, it gracefully states the information is unavailable, preventing hallucinations.

---

## 10. Authentication & Security

MeetIntel AI implements standard security practices:
- **Authentication:** Users must register and log in to access the system.
- **Password Hashing:** Passwords are never stored in plaintext; they are securely hashed before entering the database.
- **Data Isolation:** Every meeting, transcript, and vector chunk is strictly tied to a `user_id`. Repository and database queries explicitly filter by the authenticated user's ID, ensuring one user can never access another user's private meeting data.
- **Secrets Management:** API keys (Gemini, OpenAI, HuggingFace) are loaded securely via `.env` files and are never committed to the repository.

---

## 11. API

An advanced FastAPI layer exposes the core platform capabilities for potential future integration:

| Method | Endpoint | Purpose | Access Requirement |
|--------|----------|---------|--------------------|
| `GET` | `/meetings` | List all processed meetings for the user | `X-API-Key` & `X-User-Id` |
| `GET` | `/meetings/{id}` | Retrieve detailed structured insights for a specific meeting | `X-API-Key` & `X-User-Id` |
| `POST` | `/search` | Perform global semantic search across the vector knowledge base | `X-API-Key` & `X-User-Id` |
| `POST` | `/ask` | RAG-powered question answering across the knowledge base | `X-API-Key` & `X-User-Id` |

---

## 12. Integrations

The repository contains a foundation for external integrations in `api/integrations.py`:
- **Zoom Webhooks (Configuration-Ready):** Endpoints exist to handle `recording.completed` webhooks.
- **Google Meet Webhooks (Configuration-Ready):** Endpoints exist to handle Google Workspace Drive Activity pushes.

*Note: These integrations currently contain simulated/mocked download logic and require further developer implementation (OAuth setups, real API downloading) to be production-ready.*

---

## 13. Reports & Export

Users can export processed meeting intelligence in multiple formats:
- **PDF Export:** Generates a professional "Minutes of Meeting" document containing the executive summary, decisions, action items, participants, and deadlines.
- **CSV Export:** Generates tabular data for easy import into spreadsheets or project management tools.
- **DOCX Export:** Generates a Microsoft Word compatible document.

---

## 14. Project Structure

```text
MeetIntel-AI/
├── ai/                     # LLM providers, meeting analyzer, RAG, and Pydantic schemas
├── api/                    # FastAPI endpoints and integration webhooks
├── audio/                  # FFmpeg utilities and audio extraction
├── config/                 # Application configuration
├── data/                   # Default storage location for raw audio files
├── reports/                # PDF, CSV, and DOCX generation logic
├── scripts/                # Diagnostic scripts (e.g., check_gemini.py)
├── storage/                # SQLite database, SQLAlchemy models, and ChromaDB vector store
├── tests/                  # API, Auth, E2E, and Milestone test suites
├── transcription/          # Faster-Whisper and Pyannote implementation
├── ui/                     # Streamlit frontend, dashboard, meeting views, auth
├── utils/                  # Helper utilities
├── validation/             # File and input validation
├── app.py                  # Main Streamlit application entry point
├── Dockerfile              # Containerization configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 15. Installation

Follow these steps to set up MeetIntel AI locally.

### Requirements
- macOS (Apple Silicon recommended) or Linux
- Python 3.9+
- `ffmpeg` installed on your system (`brew install ffmpeg` on macOS)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/meetintel-ai.git
   cd meetintel-ai
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   OPENAI_API_KEY=your_openai_key_here
   HUGGINGFACE_TOKEN=your_hf_token_here
   API_KEY=your_custom_api_secret  # For FastAPI access
   ```
   *(Note: HuggingFace token requires you to accept the `pyannote/speaker-diarization-community-1` terms on HuggingFace).*

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```
   The application will be available at `http://localhost:8501`.
