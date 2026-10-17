# MeetIntel AI — Technical Architecture & Technology Deep-Dive Guide

**Document Version:** 2.0.0  
**Target Audience:** Students, Engineering Interns, Technical Reviewers, Software Architects  
**Prerequisites:** Basic knowledge of Python, REST APIs, and databases.

---

## Table of Contents
1. [Core Conceptual Distinctions for Beginners](#1-core-conceptual-distinctions-for-beginners)
2. [Audio & Speech Pipeline](#2-audio--speech-pipeline)
   - [FFmpeg Audio & Video Preprocessing](#21-ffmpeg-audio--video-preprocessing)
   - [Faster-Whisper Speech-to-Text Engine](#22-faster-whisper-speech-to-text-engine)
   - [Pyannote Speaker Diarization](#23-pyannote-speaker-diarization)
   - [Timestamp Alignment & Dialogue Formatter](#24-timestamp-alignment--dialogue-formatter)
3. [AI & Large Language Model Pipeline](#3-ai--large-language-model-pipeline)
   - [AI Multi-Provider Manager & Failover Engine](#31-ai-multi-provider-manager--failover-engine)
   - [Structured Schema Validation & Pydantic](#32-structured-schema-validation--pydantic)
   - [Gemini & OpenAI Integrations](#33-gemini--openai-integrations)
   - [Offline Demo Provider & Sandbox Simulator](#34-offline-demo-provider--sandbox-simulator)
4. [Storage, Vectors & RAG Architecture](#4-storage-vectors--rag-architecture)
   - [SQLite & SQLAlchemy ORM](#41-sqlite--sqlalchemy-orm)
   - [Sentence-Transformers & Embeddings](#42-sentence-transformers--embeddings)
   - [ChromaDB Vector Store](#43-chromadb-vector-store)
   - [Retrieval-Augmented Generation (RAG) Service](#44-retrieval-augmented-generation-rag-service)
5. [Enterprise Ecosystem & Integrations](#5-enterprise-ecosystem--integrations)
   - [Google Workspace & Calendar Synchronization](#51-google-workspace--calendar-synchronization)
   - [Zoom Cloud Recording Webhooks & HMAC Verification](#52-zoom-cloud-recording-webhooks--hmac-verification)
   - [Fernet AES Token Encryption at Rest](#53-fernet-aes-token-encryption-at-rest)
   - [Attendance-Aware SMTP Email Service](#54-attendance-aware-smtp-email-service)
6. [Asynchronous Workers & Automation Engine](#6-asynchronous-workers--automation-engine)
   - [Persistent Background Worker & Scheduler](#61-persistent-background-worker--scheduler)
   - [Event-Driven Workflow Rules Engine](#62-event-driven-workflow-rules-engine)
7. [API & Application Frameworks](#7-api--application-frameworks)
   - [FastAPI REST Application](#71-fastapi-rest-application)
   - [Streamlit Enterprise UI Architecture](#72-streamlit-enterprise-ui-architecture)
   - [PBKDF2 Authentication & RBAC Authorization](#73-pbkdf2-authentication--rbac-authorization)
   - [Multi-Format Document Reporting (PDF, Word, CSV)](#74-multi-format-document-reporting-pdf-word-csv)

---

# 1. Core Conceptual Distinctions for Beginners

Before diving into code, review these fundamental software distinctions that often confuse beginners during viva evaluations:

### 1.1 Frontend Feature vs. Backend Service
- **Analogy:** A restaurant dining room vs. the restaurant kitchen.
- **Frontend (Streamlit):** What the user clicks and sees (buttons, tabs, CSS styles, progress bars). It collects inputs and renders cards.
- **Backend (FastAPI, Python modules):** The heavy computation running on the server (converting audio, running Whisper, querying ChromaDB, calculating hashes).
- **Rule of Thumb:** If Streamlit crashes or the browser tab closes, the background worker continues executing in the backend.

### 1.2 UI Button vs. API Endpoint
- **UI Button:** A visual element rendered in your browser (e.g. `st.button("Approve Task")`). It handles user clicks.
- **API Endpoint:** A standardized URL over HTTP (e.g. `POST http://localhost:8000/tasks/1/approve`) that external programs or microservices can call programmatically using JSON. In MeetIntel AI, both the Streamlit UI and the FastAPI server call the same underlying repository functions.

### 1.3 Database Record vs. External Provider Record
- **Database Record:** An entry in your local SQLite table (`calendar_events` or `action_items`). You own this data; it lives in `meetintel.db`.
- **External Provider Record:** An event stored on Google Calendar or Zoom's cloud servers.
- **Why it matters:** Just because an action item exists in your database does not mean it is on Google Calendar. It only appears on Google Calendar when the external sync succeeds and returns an `external_event_id`.

### 1.4 AI-Generated Suggestion vs. Verified Fact
- **AI Suggestion:** A task or decision extracted by an LLM with a statistical probability (e.g. `confidence: 0.95`). AI can misinterpret sarcasm, assumptions, or casual banter.
- **Verified Fact:** An action item that a human Team Lead has reviewed against the verbatim transcript excerpt and clicked **Approve Task**. MeetIntel AI treats AI output as a *draft* until a human signs off.

### 1.5 Configured Integration vs. Connected Integration
- **Configured Integration:** You have typed a `CLIENT_ID` and `CLIENT_SECRET` into your `.env` file. The credentials exist on disk.
- **Connected Integration:** The OAuth 2.0 exchange has succeeded, an encrypted access token and refresh token have been received from Google or Zoom, and the connection has been tested with a live HTTP ping.

### 1.6 Queued Job vs. Completed Job
- **Queued Job:** A row in the `background_jobs` table with `status="QUEUED"`. It is waiting for the background worker to pick it up.
- **Completed Job:** A job that was executed by `PersistentBackgroundWorker`, verified with HTTP 200 from the external service, and updated to `status="COMPLETED"`.

### 1.7 Mock / Demo Response vs. Real Provider Response
- **Real Provider Response:** Sending live HTTPS traffic to Google, OpenAI, or Zoom APIs using paid credentials and receiving real external JSON.
- **Mock / Demo Response:** A locally simulated response designed to test workflow logic without requiring paid API tokens or internet access. MeetIntel AI clearly labels mock behavior with a `🧪 Sandbox Mode` or `Connected — Demo` pill.

### 1.8 Authentication vs. Authorization
- **Authentication ("Who are you?"):** Verifying identity with username and password. MeetIntel AI uses PBKDF2 hashing with salt.
- **Authorization ("What are you allowed to do?"):** Checking permissions. An `Employee` is authenticated, but not authorized to click **Approve Task** or view the **Team Directory**. Only `Team Lead` and `Admin` roles have that authority.

### 1.9 Keyword Search vs. Semantic Search
- **Keyword Search:** Exact string matching. If you search for *"revenue"*, it will only find documents containing the exact letters *r-e-v-e-n-u-e*. It will miss sentences that say *"financial turnover"* or *"sales earnings"*.
- **Semantic Search:** Meaning-based vector search. It converts sentences into mathematical coordinates in high-dimensional space. Sentences with similar meanings have high cosine similarity, even if they use completely different words.

---

# 2. Audio & Speech Pipeline

## 2.1 FFmpeg Audio & Video Preprocessing

### 1. What it is
FFmpeg is the industry-standard multimedia processing library used to decode, convert, and normalize audio and video streams.

### 2. Why the project needs it
Users upload recordings in arbitrary formats: 1080p MP4 videos from Zoom, stereo 48kHz AAC files from Google Meet, voice memos in M4A from an iPhone, or FLAC audio. Deep learning speech models require **exact audio formatting**: single-channel (mono), 16,000 samples per second (16kHz), 16-bit uncompressed PCM WAV. If fed stereo or 44.1kHz audio, speech models crash or produce garbage timestamps.

### 3. How it works in this project
When an audio/video file is uploaded, `audio/processor.py` invokes FFmpeg via `ffmpeg-python` subprocess. It strips video tracks, resamples to 16,000Hz, downmixes to 1 channel (mono), applies volume normalization, and exports a temporary `.wav` file into `data/processed/`.

### 4. Code location
- Ingestion validator: [audio/validator.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/audio/validator.py)
- Processor: [audio/processor.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/audio/processor.py)
- Invocation in pipeline: [ui/meeting.py#L75-L81](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/ui/meeting.py#L75-L81)

### 5. Input Data
Raw file path (e.g. `data/uploads/quarterly_review.mp4`).

### 6. Processing
```bash
ffmpeg -y -i input_file -vn -acodec pcm_s16le -ar 16000 -ac 1 output_processed.wav
```
- `-vn`: Drop video track (saves CPU and memory).
- `-acodec pcm_s16le`: 16-bit linear pulse-code modulation.
- `-ar 16000`: 16,000 Hz sample rate.
- `-ac 1`: 1 channel (mono).

### 7. Output Data
Path to normalized WAV: `data/processed/quarterly_review_processed.wav`.

### 8. Dependent Components
- Faster-Whisper Transcriber (`transcription/whisper_engine.py`).
- Pyannote Speaker Diarizer (`transcription/diarization.py`).

### 9. How to test it
Run automated tests or run standalone in terminal:
```bash
PYTHONPATH=. .venv/bin/pytest tests/test_e2e.py
```

### 10. Common Failure Conditions
- **Missing FFmpeg Binary:** If `ffmpeg` is not installed on the host operating system, the subprocess throws `FileNotFoundError`.
- **Corrupted Input File:** If a user uploads an invalid file, FFmpeg returns exit code 1 with "Invalid data found when processing input".

### 11. Known Limitations
Very large files (e.g., a 4-hour 4K recording) require significant disk space during WAV decompression (~115MB per hour of 16kHz mono audio).

---

## 2.2 Faster-Whisper Speech-to-Text Engine

### 1. What it is
Faster-Whisper is a reimplementation of OpenAI's Whisper model utilizing **CTranslate2**, a fast inference engine for Transformer models.

### 2. Why the project needs it
Original OpenAI Whisper running in PyTorch is slow on standard laptops and consumes high memory. Faster-Whisper runs up to 4x faster and uses up to 70% less RAM through 8-bit quantization (`int8`), allowing high-accuracy transcription locally without cloud API costs or privacy risks.

### 3. How it works in this project
`transcription/whisper_engine.py` initializes the `WhisperModel`. It loads model weights (default: `small`, configurable in `.env`), activates Voice Activity Detection (Silero VAD) to strip silent pauses, and transcribes audio into segmented chunks with start/end millisecond timestamps.

### 4. Code location
- Engine: [transcription/whisper_engine.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/transcription/whisper_engine.py)
- Configuration: `WHISPER_MODEL=small` in `.env`

### 5. Input Data
Path to 16kHz mono WAV file.

### 6. Processing
- Model initializes with `compute_type="int8"` on CPU (or `float16` on CUDA GPU).
- Audio is sliced into 30-second windows.
- VAD filtering (`vad_filter=True`) removes non-speech background noise.
- Beam search decoding transcribes acoustic features into text tokens.

### 7. Output Data
List of dictionary segments:
```python
[
    {"start": 0.0, "end": 4.5, "text": "Welcome everyone to our security review."},
    {"start": 4.8, "end": 9.2, "text": "I will finish the OAuth integration by Friday."}
]
```

### 8. Dependent Components
- Dialogue Alignment (`transcription/alignment.py`).
- LLM Analyzer (`ai/meeting_analyzer.py`).

### 9. How to test it
```bash
PYTHONPATH=. .venv/bin/python test_transcribe.py
```

### 10. Common Failure Conditions
- **First-run download timeout:** On first run, Hugging Face model weights (~500MB) are downloaded. If internet disconnects, model load fails.
- **Low RAM:** Models larger than `small` (`medium`, `large-v3`) can exhaust RAM on low-spec systems.

### 11. Known Limitations
Does not natively recognize *who* is speaking; it only knows *what* was said and *when*. Speaker identity requires diarization.

---

## 2.3 Pyannote Speaker Diarization

### 1. What it is
Pyannote.audio is an open-source neural acoustic toolkit for **Speaker Diarization** (answering *"Who spoke when?"*).

### 2. Why the project needs it
A meeting transcript where all speech is lumped together is useless for assigning accountability. Diarization clusters vocal characteristics into distinct speaker tracks (`Speaker 0`, `Speaker 1`), allowing MeetIntel AI to know that Alex spoke one sentence and Sarah spoke another.

### 3. How it works in this project
`transcription/diarization.py` checks for `HUGGINGFACE_TOKEN`. If present, it loads `pyannote/speaker-diarization-3.1`. It passes the audio through a Convolutional/Recurrent neural network that computes voice embeddings and performs agglomerative hierarchical clustering to output speaker timeline segments. If no token is provided, a graceful energy-based fallback segments audio turns without crashing.

### 4. Code location
- [transcription/diarization.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/transcription/diarization.py)

### 5. Input Data
Path to 16kHz mono WAV file.

### 6. Processing
- Neural feature extraction on 5-second overlapping sliding windows.
- PyanNet voice embedding projection.
- Binarization and clustering of speaker identity vectors.

### 7. Output Data
Timeline of speaker turns:
```python
[
    {"start": 0.0, "end": 4.2, "speaker": "Speaker 1"},
    {"start": 4.5, "end": 9.5, "speaker": "Speaker 2"}
]
```

### 8. Dependent Components
- Timestamp Alignment (`transcription/alignment.py`).

### 9. How to test it
Verify through full pipeline tests: `PYTHONPATH=. .venv/bin/pytest tests/test_milestone2.py`.

### 10. Common Failure Conditions
- **Invalid Hugging Face Token:** Pyannote weights are gated on Hugging Face. The user must accept the user conditions for `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0`.
- **Heavy overlapping speech:** When two people talk over each other simultaneously, diarization may misattribute words to the dominant voice.

### 11. Known Limitations
Pyannote identifies that voice A is distinct from voice B (`Speaker 1` vs `Speaker 2`), but does not know their real names until aligned with meeting metadata or dialogue turns.

---

## 2.4 Timestamp Alignment & Dialogue Formatter

### 1. What it is
The synchronization module that merges Whisper's word transcripts with Pyannote's speaker timeline.

### 2. Why the project needs it
Whisper produces text segments with word timestamps. Pyannote produces speaker identity segments. Because their window intervals never align perfectly (e.g. Whisper says words from 2.1s–5.8s, while Pyannote says Speaker 1 spoke from 1.8s–5.5s), an alignment algorithm is required to calculate temporal overlap and attribute each spoken sentence to the correct person.

### 3. How it works in this project
`transcription/alignment.py` iterates over Whisper segments. For each segment, it calculates the mathematical intersection window with Pyannote turns. The speaker with the greatest temporal overlap is assigned to the sentence. `transcription/formatter.py` then cleans disfluencies (stutters, repeated filler words) in "Clean Verbatim" mode.

### 4. Code location
- Alignment: [transcription/alignment.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/transcription/alignment.py)
- Formatter: [transcription/formatter.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/transcription/formatter.py)

### 5. Input Data
Whisper text segments + Pyannote speaker turns.

### 6. Output Data
Aligned database objects (`TranscriptSegment`):
```python
TranscriptSegment(
    speaker="Alex Chen",
    start=36.0,
    end=65.0,
    text="I will complete the OAuth 2.0 PKCE integration by this Friday.",
    confidence=0.99
)
```

### 7. Dependent Components
- Database persistence (`storage/repository.py:save_transcript()`).
- AI Meeting Analyzer (`ai/meeting_analyzer.py`).

---

# 3. AI & Large Language Model Pipeline

## 3.1 AI Multi-Provider Manager & Failover Engine

### 1. What it is
An enterprise resilience manager that orchestrates calls across multiple AI providers (Google Gemini, OpenAI GPT-4o, and Offline Demo Provider) with automatic failover, circuit breaking, and cooldown tracking.

### 2. Why the project needs it
Third-party cloud AI APIs suffer from rate limits (HTTP 429), temporary outages (HTTP 503), quota expirations, and network timeouts. In a corporate environment, a meeting analysis cannot fail simply because one vendor had a 30-second glitch.

### 3. How it works in this project
`ai/provider_manager.py` maintains an in-memory health dictionary `_provider_health`. When an LLM call is requested, it builds an execution chain based on `.env` configuration (e.g. `gemini` -> `openai`). If Gemini throws a `TransientAIError` or `QuotaExhaustedError`, the manager marks Gemini as unhealthy for 120 seconds, logs a warning, and immediately re-executes the prompt against OpenAI without interrupting the user.

```
                    ┌────────────────────────┐
                    │ LLM Request Triggered  │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ Check Provider Health  │
                    │   (Cooldown Cache)     │
                    └───────────┬────────────┘
                                │
            ┌───────────────────┴───────────────────┐
            ▼                                       ▼
  [ Try Primary: Gemini ]                 [ Gemini on Cooldown? ]
            │                                       │
      Success? ──► Return Output                    │
            │ (No: 429/503/Timeout)                 │
            ▼                                       │
  [ Mark Gemini Unhealthy ]                         │
  [    for 120 seconds    ]                         │
            │                                       │
            └───────────────────┬───────────────────┘
                                ▼
                    [ Try Fallback: OpenAI ]
                                │
                          Success? ──► Return Output
                                │ (No)
                                ▼
                    [ DEMO_MODE=true in .env? ]
                       ├── YES ──► Execute DemoProvider
                       └── NO  ──► Raise Descriptive Error
```

### 4. Code location
- Provider Manager: [ai/provider_manager.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/ai/provider_manager.py)
- Base Classes & Exceptions: [ai/base.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/ai/base.py)

### 5. Input Data
Method name (`generate_insights`, `ask_question`, `rag_ask_question`) and prompt arguments.

### 6. Processing
- Loops through healthy providers in order: `gemini` -> `openai`.
- Catches `TransientAIError`, `QuotaExhaustedError`, and `AuthError`.
- Records `st.session_state['last_ai_provider_used'] = provider_name` for UI transparency.

### 7. Output Data
Structured response dictionary or text answer.

### 8. How to test it
```bash
PYTHONPATH=. .venv/bin/pytest tests/test_milestone2.py::test_rate_limit_and_failover
```

---

## 3.2 Structured Schema Validation & Pydantic

### 1. What it is
Pydantic model enforcement ensuring that LLM text responses adhere to a strict, typed JSON schema before touching the database.

### 2. Why the project needs it
LLMs are probabilistic text generators. Left unconstrained, an LLM might return Markdown, chatty commentary (*"Here is your summary..."*), missing fields, or invalid types. Pydantic guarantees that keys like `action_items`, `decisions`, `evidence_excerpt`, and `deadline` always exist and match expected types.

### 3. How it works in this project
`ai/schemas.py` defines `MeetingInsightsSchema`, `ActionItemSchema`, `DecisionSchema`, `ParticipantSchema`, `DeadlineSchema`, and `PrioritySchema`. The prompt explicitly instructs the LLM to output valid JSON matching this schema. The returned string is parsed and validated via `MeetingInsightsSchema.model_validate_json()`.

### 4. Code location
- Schemas: [ai/schemas.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/ai/schemas.py)
- System Prompt: [ai/prompts/meeting_intelligence_prompt.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/ai/prompts/meeting_intelligence_prompt.py)

### 5. Schema Definition
```python
class ActionItemSchema(BaseModel):
    task: str
    description: Optional[str]
    assigned_to: str
    assignment_status: str  # 'Assigned', 'Needs assignment', 'Suggested'
    deadline: Optional[str]
    priority: str          # 'Low', 'Medium', 'High', 'Urgent'
    confidence: float
    evidence_excerpt: str  # Exact sentence from transcript
    dependencies: List[str]
    estimated_effort_hours: Optional[float]
```

### 6. Output
Validated Python dictionary inserted safely into SQLite models.

---

## 3.3 Gemini & OpenAI Integrations

### 1. What they are
Direct API integrations for Google's Gemini models (`gemini-3.6-flash`, `gemini-1.5-pro`) and OpenAI models (`gpt-4o`, `gpt-4o-mini`).

### 2. How they work in this project
- **Gemini (`ai/gemini.py`):** Uses official `google-genai` / `google-generativeai` SDK. Implements exponential backoff retries via `tenacity`.
- **OpenAI (`ai/openai_provider.py`):** Uses official `openai` Python SDK with JSON mode enabled (`response_format={"type": "json_object"}`).

---

# 4. Storage, Vectors & RAG Architecture

## 4.1 SQLite & SQLAlchemy ORM

### 1. What it is
SQLAlchemy is an Object-Relational Mapping (ORM) library that maps Python classes to relational database tables. The default database engine is SQLite (`meetintel.db`), with full PostgreSQL compatibility.

### 2. Why the project needs it
To store structured meeting records, multi-user accounts, password hashes, action item execution statuses, audit events, and background jobs with ACID transaction guarantees.

### 3. Database Schema Overview
```
┌──────────────────┐       1:N       ┌──────────────────┐
│  organizations   ├────────────────►│      users       │
└────────┬─────────┘                 └────────┬─────────┘
         │ 1:N                                │ 1:N
         ▼                                    ▼
┌──────────────────┐       1:N       ┌──────────────────┐
│     meetings     ├────────────────►│   action_items   │
└────────┬─────────┘                 └────────┬─────────┘
         │                                    │ 1:1
         ├──────────────► transcript_segments │
         ├──────────────► decisions           ▼
         ├──────────────► participants  ┌──────────────────┐
         ├──────────────► deadlines     │ calendar_events  │
         └──────────────► priorities    └──────────────────┘
```

### 4. Code location
- Engine & Session: [storage/database.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/storage/database.py)
- Models: [storage/models.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/storage/models.py)
- Repository Functions: [storage/repository.py](file:///Users/haricharan/Documents/Milestone%201/AI%20Powered%20Audio%20Processing%20&%20Transcription/storage/repository.py)

---

## 4.2 Sentence-Transformers & Embeddings

### 1. What it is
A local embedding service that turns text into dense 384-dimensional mathematical vectors using the `all-MiniLM-L6-v2` neural network model.

### 2. Why the project needs it
To perform semantic search and RAG retrieval across meetings without sending private transcripts to third-party embedding APIs.

### 3. How it works
`ai/embeddings.py` loads the model. When passed a list of sentences, it outputs 384 floating-point numbers per sentence representing their semantic meaning in vector space.

---

## 4.3 ChromaDB Vector Store

### 1. What it is
ChromaDB is an open-source, embedded vector database designed for AI embeddings.

### 2. Why the project needs it
Standard relational SQL queries cannot perform fast nearest-neighbor cosine similarity searches over millions of words. ChromaDB indexes high-dimensional vectors with sub-millisecond search times.

### 3. Multi-Tenant Security in ChromaDB
Every chunk stored in ChromaDB contains metadata:
```python
{
    "meeting_id": "demo-meeting-q3-security",
    "user_id": "alex-uuid",
    "org_id": "org-default-001",
    "content_type": "transcript",
    "start_time": 36.0,
    "end_time": 65.0
}
```
When querying, `storage/vector_store.py` applies a mandatory `where` filter:
```python
where = {"org_id": org_id}
```
This guarantees that Organization A can never retrieve vector embeddings belonging to Organization B.

---

## 4.4 Retrieval-Augmented Generation (RAG) Service

### 1. What it is
The system that answers user questions grounded in meeting transcripts.

### 2. How it works step-by-step
1. User asks: *"Who is working on the OAuth integration?"*
2. `EmbeddingService` converts the question into a 384-dimensional query vector.
3. `ChromaDB` finds the top 5 closest matching transcript chunks by cosine distance.
4. The system constructs a grounded prompt:
   ```
   Context Excerpts from Verified Meeting Transcripts:
   [Excerpt 1] Alex Chen: "I will complete the OAuth 2.0 PKCE integration by Friday."
   
   User Question: Who is working on the OAuth integration?
   Instruction: Answer strictly using the context above. If not mentioned, state you do not know.
   ```
5. The LLM generates the answer and returns source citations.

---

# 5. Enterprise Ecosystem & Integrations

## 5.1 Google Workspace & Calendar Synchronization

- **OAuth 2.0 Flow:** Implemented in `integrations/google_workspace.py`. Directs users to Google's consent screen and exchanges the code at `GET /api/google/oauth/callback`.
- **Calendar Event Scheduling:** When an action item with a deadline is approved, `sync_task_to_calendar()` creates an event with 24-hour and 1-hour email reminders.
- **Idempotency Protection:** Uses a unique key `cal_sync_{task_id}` to prevent duplicate events.

## 5.2 Zoom Cloud Recording Webhooks & HMAC Verification

- **Endpoint:** `POST /api/zoom/webhook`.
- **HMAC-SHA256 Signature Verification:** Hashes timestamp + request body against `ZOOM_WEBHOOK_SECRET` and compares using `secrets.compare_digest`.
- **Replay Protection:** Rejects any webhook whose timestamp differs from server time by more than 300 seconds (5 minutes).

## 5.3 Fernet AES Token Encryption at Rest

- Stored in `integrations/crypto.py`.
- Encrypts OAuth access tokens, refresh tokens, and webhook secrets using 32-byte Fernet AES symmetric keys derived from `SECRET_KEY`.
- Plaintext secrets are never stored in `meetintel.db` or output in application logs.

## 5.4 Attendance-Aware SMTP Email Service

- Stored in `integrations/email_service.py`.
- Detects absent members from verified attendance records.
- Prepares a personalized summary email containing only approved deliverables.
- Enforces **review-before-send gating**: an email cannot be dispatched until a manager approves it.

---

# 6. Asynchronous Workers & Automation Engine

## 6.1 Persistent Background Worker & Scheduler

- Stored in `storage/background_worker.py`.
- Polls the `background_jobs` table for jobs with `status="QUEUED"`.
- **Exponential Backoff with Jitter:** When an external API fails, the retry delay is calculated as $2^{\text{retry}} \times 10 \times \text{jitter}$ seconds to prevent hammering the service.
- **Zombie Recovery:** Detects jobs stuck in `RUNNING` for over 15 minutes and resets them to `RETRYING`.

## 6.2 Event-Driven Workflow Rules Engine

- Defined by `WorkflowRule` in `storage/models.py`.
- Triggers actions automatically upon system events (e.g., when a task is approved, schedule a calendar event; when a task is blocked, flag downstream dependencies).

---

# 7. API & Application Frameworks

## 7.1 FastAPI REST Application

- Located at `api/main.py` and `api/integrations.py`.
- Serves 19 REST endpoints for meetings, tasks, decisions, audit logs, semantic search, RAG, and webhooks.
- Authenticated via `X-API-Key` and `x-user-id` headers.
- CORS middleware enabled for web and mobile clients.

## 7.2 Streamlit Enterprise UI Architecture

- Entry point: `app.py`.
- 16 modular view files in `ui/`.
- Styling: `ui/styles.py` applies a cohesive enterprise Violet/Lavender design system with subtle surfaces, Lucide SVG line icons, and accessible contrast.
- Fully role-gated navigation in `ui/navigation.py`.

## 7.3 PBKDF2 Authentication & RBAC Authorization

- Password hashing: `storage/auth.py` executes PBKDF2 HMAC SHA-256 with 100,000 iterations and a 16-byte cryptographically secure random salt.
- Server-side RBAC: Enforced in `api/main.py` and Streamlit views. Only `Admin` and `Team Lead` roles can approve tasks, reassign ownership, or access governance logs.

## 7.4 Multi-Format Document Reporting (PDF, Word, CSV)

- **PDF (`reports/pdf.py`):** Uses `fpdf2` with bundled DejaVu UTF-8 fonts to avoid character encoding crashes.
- **Word (`reports/docx.py`):** Uses `python-docx` to produce corporate Minutes of Meeting documents.
- **CSV (`reports/csv.py`):** Uses Python standard `csv` / `pandas` to export structured task and decision spreadsheets.
