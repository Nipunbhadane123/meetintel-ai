# MeetIntel AI — Enterprise Meeting-to-Execution Automation Platform

> **"Turn every meeting into accountable action, automated follow-up, and measurable progress."**

MeetIntel AI is a production-grade enterprise application that evolves meeting intelligence from passive transcripts and summaries into an **accountable execution and organizational operations engine**.

The platform automates the end-to-end lifecycle of meeting outcomes:
```
Meeting Recording / Transcript
              ↓
      Validated Transcript
              ↓
Speaker & Participant Dialogue Mapping
              ↓
  AI Meeting Analysis & Evidence Extraction
              ↓
  Proposed Decisions & Action Items (with Excerpts)
              ↓
   Human Approval Gating (Team Lead / Admin)
              ↓
     Task & Commitment Creation
              ↓
Google Calendar Reminders & Attendance-Aware Follow-ups
              ↓
     Progress Tracking & Blocker Resolution
              ↓
     Audit Trail & Organizational Memory
```

---

## 📚 Official Learning Guides & Documentation

Complete documentation is organized for beginners, developers, and evaluators in the `docs/` directory:

| Guide | File | Description |
| :--- | :--- | :--- |
| **Vercel Deployment Audit** | [`docs/VERCEL_DEPLOYMENT_AUDIT.md`](docs/VERCEL_DEPLOYMENT_AUDIT.md) | Component-by-component architectural audit & runtime feasibility analysis. |
| **Vercel Deployment Guide** | [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) | Step-by-step production deployment manual for Vercel, PostgreSQL, and OAuth. |
| **Production Readiness Checklist** | [`docs/PRODUCTION_CHECKLIST.md`](docs/PRODUCTION_CHECKLIST.md) | Pre-flight security, persistence, secrets, and verification matrix. |
| **Deployment Troubleshooting** | [`docs/DEPLOYMENT_TROUBLESHOOTING.md`](docs/DEPLOYMENT_TROUBLESHOOTING.md) | Runbook for Vercel builds, OAuth callbacks, database pooling, and quotas. |
| **Documentation Index** | [`docs/README.md`](docs/README.md) | Master index and recommended learning path for beginners. |
| **Complete User Manual** | [`docs/MEETINTEL_AI_USER_MANUAL.md`](docs/MEETINTEL_AI_USER_MANUAL.md) | Exhaustive operator handbook for every page, button, form, and feature. |
| **Practical Tutorials** | [`docs/PRACTICAL_TUTORIALS.md`](docs/PRACTICAL_TUTORIALS.md) | 10 hands-on step-by-step walkthroughs of major workflows. |
| **Technical Deep-Dive** | [`docs/FEATURES_AND_TECHNOLOGY_EXPLAINED.md`](docs/FEATURES_AND_TECHNOLOGY_EXPLAINED.md) | Engineering explanations of Faster-Whisper, Pyannote, RAG, and security. |
| **End-to-End Workflows** | [`docs/END_TO_END_WORKFLOWS.md`](docs/END_TO_END_WORKFLOWS.md) | Architectural data flow diagrams and sequence charts. |
| **Feature Inventory** | [`docs/FEATURE_INVENTORY.md`](docs/FEATURE_INVENTORY.md) | Status matrix of all 62 features discovered across the codebase. |
| **Visual Feature Map** | [`docs/FEATURE_MAP.md`](docs/FEATURE_MAP.md) | Hierarchical feature breakdown and service dependency matrices. |
| **QA Verification Checklist** | [`docs/FEATURE_VERIFICATION_CHECKLIST.md`](docs/FEATURE_VERIFICATION_CHECKLIST.md) | Manual test cases and 69 passing automated pytest results. |
| **Viva & Evaluation Guide** | [`docs/PROJECT_PRESENTATION_AND_VIVA.md`](docs/PROJECT_PRESENTATION_AND_VIVA.md) | Technical defense presentation and 15 essential viva Q&As. |

---

## 1. Architecture Overview

```
+---------------------------------------------------------------------------------+
|                                 USER WORKSPACE                                  |
|   Employee Workspace  |  Team Lead Workspace  |  Organization Admin Workspace   |
|   (My Tasks, Due)     |  (Approvals, Blocker) |  (Integrations, Retention, Org) |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                               PRESENTATION TIER                                 |
|  Streamlit SaaS Frontend (Port 8501) | Next.js 16 Web Application (Port 3000)  |
|  FastAPI REST API Engine (Port 8000) | ROI Telemetry & Eisenhower Matrix (2x2)  |
|  Light/Dark Dynamic Theme Tokens     | 1-Click Slack / Teams Debrief Exporter   |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                           INTELLIGENCE & AGENT ENGINE                           |
|  - MeetingAnalyzer (Pydantic v2 Schema Validation, Anti-Injection Isolated Data)|
|  - AI Provider Manager (Gemini 3.8 / OpenAI GPT-4o-mini / Local Demo Engine)    |
|  - RAG Service (Cross-Meeting Semantic Search, Grounded Source Citations)       |
|  - AI Quality Center (JiWER WER, Action F1, Owner Accuracy, Grounding Checks)   |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                       SAAS INTEGRATIONS & AUTOMATION                            |
|  - Google Workspace: OAuth 2.0, Google Meet Artifacts, Google Calendar Sync     |
|  - Zoom Service: HMAC-SHA256 Signed Webhook, Replay Protection, Cloud Ingestion |
|  - Email Dispatcher: Attendance-Aware Absent Follow-up, Review-Before-Send Gating|
|  - Persistent Background Worker: Exponential Backoff, Jitter, Idempotent Queue  |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                            DATA & PERSISTENCE TIER                              |
|  - Relational Database: SQLite (Local) / PostgreSQL Compatible (SQLAlchemy ORM)  |
|  - Vector Store: ChromaDB with Tenant-Isolated Namespace Chunks                 |
|  - File Storage: data/uploads, data/processed, reports/                         |
+---------------------------------------------------------------------------------+
```

---

## 2. Core Capabilities & Workflows

### A. Structured Action-Item Extraction & Assignment Reliability
- **Verbatim Evidence Grounding**: Every proposed action item and decision captures the exact quote from the transcript.
- **Reliable Assignee Resolution**: Maps dialogue names against organization member directories.
- **Ambiguity Protection**:
  - Ambiguous owner -> Flagged as `Needs assignment` and routed to Team Lead review.
  - Vague deadline -> Preserved verbatim (e.g. `sometime soon`) with `deadline_ambiguous: true`. Dates are never hallucinated.
- **Approval Workflow**:
  - `Draft` -> `Pending Approval` -> `Approved` -> `Scheduled` -> `In Progress` -> `Completed` / `Blocked` / `Rejected`.
- **Role Permissions**:
  - **Employee**: View assigned tasks, update status, add completion notes, view relevant decisions.
  - **Team Lead**: Approve, reject, reassign tasks, resolve blockers.
  - **Admin**: Configure integrations, tenant policies, audit logs.

### B. Enterprise SaaS Integrations (Google Meet, Zoom, Google Calendar, Email)
1. **Google Workspace**:
   - OAuth 2.0 consent with CSRF state protection.
   - Discovers Google Meet recordings and transcripts in Google Drive. If a transcript is already present, it is imported directly without re-transcribing.
   - Idempotent Google Calendar synchronization for approved tasks with configurable reminders (24h, 1h before deadline).
   - Disconnected fallback: Retains approved task locally with `Calendar synchronization pending` status.
2. **Zoom**:
   - HMAC-SHA256 signed webhook verification (`x-zm-signature` and timestamp) with 5-minute replay attack defense.
   - Handles `endpoint.url_validation` challenge responses.
   - Idempotent ingestion of cloud recordings on `recording.completed` event.
3. **Attendance-Aware Follow-up**:
   - Determines absence from verified participant records or organizer input (never inferred from silence).
   - Prepares personalized follow-up with executive summary, relevant decisions, assigned deliverables, and confirmed deadlines.
   - Review-before-send gating by default.
   - Tracks: `Pending` -> `Approved` -> `Sent` -> `Delivered` -> `Acknowledged`.
4. **Integration Center**:
   - Status badges: Connected / Not connected / Needs attention / Mock/Demo Mode.
   - Connection testing, disconnect/reconnect, prerequisite setup guides. Never leaks credentials.

### C. Pre-Meeting Intelligence & Preparation Briefs
- Generates an executive briefing before upcoming meetings.
- Aggregates previous meeting summaries, outstanding tasks, unresolved decisions, and known blockers.
- Suggests an evidence-grounded agenda and discussion prompts. Clearly labels AI suggestions.

### D. Decision Register & Traceability
- Dedicated searchable register of decisions.
- Captures agreement, rationale, alternatives considered, source meeting, and evidence excerpts.
- Supports superseding workflows with audit logging.

### E. AI Accuracy, Benchmarking & Trust (AI Quality Center)
- **Word Error Rate (WER)**: Measured using JiWER on audio transcription.
- **Action Item Precision, Recall, and F1**: Evaluated against labeled benchmarks.
- **Assignment & Deadline Accuracy**: Verified against ambiguous and clean dialogue.
- **Evidence Grounding Rate**: Confirms generated items map to source transcripts.
- **Prompt-Injection Defense**: 100% isolation of untrusted transcript content from system instructions.

### F. Meeting Financial Cost & ROI Telemetry Engine
- **Financial Spend Computation**: Quantifies meeting financial burn rate based on attendee headcounts, duration, and customizable team compensation rates ($50 - $150/hr).
- **Decision & Execution Velocity**: Calculates dollar cost per ratified decision and action-item density per meeting hour.
- **ROI Efficiency Letter Grading**: Dynamically rates meetings (Grades A/B/C/D) based on decision and action outcome velocity vs. organizational cost, identifying high-cost or unproductive meetings.
- **1-Click Executive Debrief & MoM Exporter**:
  - **Slack Block Kit**: Generates structured, production-ready Slack JSON blocks with KPI callout stats and copy-to-clipboard functionality.
  - **Microsoft Teams / Markdown**: Creates formatted executive briefings ready for email dispatch or channel posting.
  - **Direct Webhook Dispatch**: One-click simulated or real webhook dispatch for automated post-meeting broadcasts.

### G. Eisenhower Priority Matrix (2x2) & Date Parsing
- **Dynamic 2x2 Matrix View**: Real-time task view categorized by impact and urgency:
  - **Q1: Do First (Urgent & High Impact)**: Immediate blocking issues and high-priority commitments.
  - **Q2: Schedule (Strategic / Important)**: Medium/long-term architecture and process improvements.
  - **Q3: Quick Wins (Low Impact / Low Effort)**: Fast turnaround administrative tasks.
  - **Q4: Backlog / Revisit**: Optional deliverables for future sprint refinement.
- **Natural Language Relative Date Parser**:
  - Automatically translates conversational deadlines ("tomorrow", "by Friday", "in 3 days") into valid ISO-8601 timestamps.
  - Live visual urgency chips ("Due in 2 days", "Due today", "Overdue") with smart urgency sorting.

---

## 3. Technology Stack

- **Modern Web Application**: Next.js 16 (App Router), React 19, TypeScript 5, Lucide React, Turbopack.
- **Interactive SaaS Frontend**: Streamlit 1.62+ with custom CSS design tokens (responsive light/dark surfaces).
- **Backend API Engine**: FastAPI 0.141+ with Pydantic v2 schemas and health checks (`/health/live`, `/health/ready`).
- **Database & Persistence**: SQLAlchemy 2.0+ (SQLite development, PostgreSQL production).
- **Speech Processing**: Faster-Whisper (CTranslate2), Pyannote.Audio 3.1+, FFmpeg.
- **Vector Search & RAG**: ChromaDB 1.5+, Sentence-Transformers.
- **AI Providers**: Google Gemini, OpenAI GPT-4o-mini, Local Deterministic DemoProvider.
- **Security & Cryptography**: Fernet token encryption, HMAC-SHA256 signature verification, PBKDF2 password hashing.

---

## 4. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Key environment variables:
```ini
# Application Secrets
SECRET_KEY=meetintel-enterprise-secret-key-2026
API_KEY=dev-secret-key
DEMO_MODE=false
ALLOW_OFFLINE_FALLBACK=true

# Database (SQLite default, or PostgreSQL)
DATABASE_URL=sqlite:///meetintel.db

# AI Provider Configuration
AI_PRIMARY_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Speech & Diarization
WHISPER_MODEL=small
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Google Workspace Integration
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8501/api/google/oauth/callback

# Zoom Integration
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret
ZOOM_WEBHOOK_SECRET=your_zoom_webhook_secret

# Email Dispatcher (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=notifications@yourorg.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=notifications@meetintel.ai
```

---

## 5. Local Setup & Execution

### 1. Create Virtual Environment and Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize Database & Safe Migrations
```bash
python -c "from storage.database import init_db; init_db()"
```

### 3. Start Streamlit Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 4. Start FastAPI Service & Webhook Listener (Optional)
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)  
Health Check: [http://localhost:8000/health/live](http://localhost:8000/health/live)

### 5. Start Background Queue Worker (Optional)
```bash
python storage/background_worker.py
```

### 6. Start Next.js Modern Web Application (Port 3000)
```bash
cd web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 7. Windows 1-Click Launchers
Convenient pre-configured batch scripts are provided in the repository root:
- `run_all.bat` — Starts FastAPI, Streamlit, and Next.js concurrently.
- `run_web.bat` — Launches Next.js Web Application on `http://localhost:3000`.
- `run_backend.bat` — Launches FastAPI REST API on `http://localhost:8000`.
- `run_streamlit.bat` — Launches Streamlit SaaS Dashboard on `http://localhost:8501`.

---

## 6. Testing & Acceptance Criteria

Run the automated test suite covering all enterprise workflows, analytics, and acceptance criteria:
```bash
pytest tests/ -k "not test_rag"
```

Test Results Breakdown:
- `tests/test_analytics_and_dates.py`: Meeting cost calculation, ROI efficiency grading, relative date parsing, and Slack export formatting [7 passed]
- `tests/test_api.py`: FastAPI endpoints, task approvals, search, health checks, ROI analytics, and Slack export [6 passed]
- `tests/test_auth.py`: PBKDF2 password hashing and salt verification [1 passed]
- `tests/test_e2e.py`: End-to-end meeting analysis pipeline [1 passed]
- `tests/test_eval_metrics.py`: WER, CER, F1 score, precision, and recall evaluations [4 passed]
- `tests/test_milestone2.py`: RAG and chunking validation [6 passed]
- `tests/test_milestone3.py`: Storage schemas, task lifecycle, and follow-ups [14 passed]
- `tests/test_milestone4.py`: Report generation, PDF export, and executive briefing [17 passed]
- `tests/test_enterprise_workflows.py`:
  1. Validated action-item extraction with verbatim evidence
  2. Ambiguous ownership handling (`Needs assignment`)
  3. Ambiguous deadline preservation
  4. Task approval idempotency
  5. Calendar duplicate event prevention
  6. Disconnected calendar local task retention
  7. Absent employee authorized information filtering
  8. Failed email visibility and retry tracking
  9. Zoom webhook replay and duplicate protection
  10. Recording deduplication detection
  11. OAuth token expiry handling
  12. Multi-tenant organization isolation
  13. Access-controlled RAG retrieval
  14. Prompt-injection defense in meeting transcripts
  15. Low-confidence task human review routing
  16. Task change calendar synchronization
  17. Audit trail logging for actions
  18. Demo mode safety isolation
  19. Theme tokens accessibility
  20. End-to-end seeded enterprise scenario execution
  [20 passed]

**Total: 76 tests passing with zero errors.**

---

## 7. Live Examiner Demonstration Walkthrough Script

Follow this concise 5-minute script to demonstrate the complete end-to-end story to examiners:

### Step 1: Login & Identity Switching
1. Navigate to [http://localhost:8501](http://localhost:8501).
2. Log in with:
   - Username: `admin`
   - Password: `admin123`
3. Point out the **Acme Global Technologies** multi-tenant organization banner and the active role (`Admin`).

### Step 2: Seed Enterprise Demonstration Data
1. Click **Settings** in the sidebar.
2. Under **Fast Role & Identity Switcher**, point out the team members (`Sarah Jenkins - Team Lead`, `Alex Chen - Employee`, `Priya Sharma - QA`).
3. Click the primary button: **✦ Seed Enterprise Demonstration Scenario**.
4. The system immediately creates the realistic **Q3 Architecture & Security Alignment** scenario.

### Step 3: Meeting Intelligence & Grounded Action Items
1. Click **Meetings** -> Select **Q3 Architecture & Security Alignment**.
2. Show the **Executive Summary**, **Emotional Tone**, and **Speakers**.
3. Switch to the **Action Items** tab:
   - Highlight that each task includes **Transcript Source Evidence** (e.g., `"Alex Chen: I will complete the OAuth 2.0 PKCE integration by this Friday."`).
   - Show the confidence score (`99% Grounded`).
   - Show the ambiguous task: `"Update developer security documentation"` -> correctly flagged with `⚠️ Needs assignment` and confidence warning (`65%`).
   - Click **✓ Approve** on Alex Chen's task -> show the toast confirming Google Calendar synchronization!

### Step 4: Decision Register & Superseding
1. Click **Decisions** in the sidebar.
2. Show the decision: `"Mandate OAuth 2.0 with PKCE"`.
3. Highlight the **Rationale**, **Alternatives Considered**, and exact verbatim **Source Transcript Excerpt**.
4. Show how a Team Lead can supersede a decision when policies evolve, preserving full revision history.

### Step 5: Employee Execution & Calendar Reminders
1. Go to **Settings** -> Switch identity to **Alex Chen (Employee)**.
2. Click **My Tasks**:
   - Alex only sees deliverables assigned to him (`Complete OAuth 2.0 PKCE integration`).
   - Show the calendar indicator: `✓ Synced to Calendar`.
   - Update the status to `Completed` and enter notes.
   - Open the **Audit Trail** tab to show that the approval, reassignment, and status updates are permanently logged.

### Step 6: Attendance-Aware Absent Follow-up
1. Switch identity to **Sarah Jenkins (Team Lead)**.
2. Click **Follow-ups** in the sidebar.
3. Show the draft prepared for **Elena Rostova** (who was absent due to client deployment):
   - Notice that Elena's draft contains only approved tasks and relevant decisions.
   - Point out the **Review-Before-Send Gating**.
   - Click **Approve & Dispatch Email** -> Show successful delivery.

### Step 7: Pre-Meeting Intelligence Brief
1. Click **Meeting Prep** in the sidebar.
2. Select baseline meeting and click **Generate Preparation Brief**.
3. Show the executive briefing:
   - Summary of previous session
   - Known blockers (e.g. database pool dependency)
   - Outstanding commitments
   - Proposed agenda and discussion points (clearly marked as AI suggestions).

### Step 8: Integration Center & AI Quality Center
1. Click **Integrations**: Show verified statuses for Google Meet, Zoom, Google Calendar, and Email. Run a **Connection Test**.
2. Click **AI Quality**: Run the **Reproducible AI Benchmark Evaluation** -> show the live measured JiWER WER, F1 score, 100% owner accuracy, and 100% prompt-injection defense rate.

---

## 8. Docker Deployment

### Build Container
```bash
docker build -t meetintel-ai:2.0 .
```

### Run Container
```bash
docker run -d -p 8501:8501 -p 8000:8000 --env-file .env meetintel-ai:2.0
```

---

## 9. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
