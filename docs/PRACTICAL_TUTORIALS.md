# MeetIntel AI — Step-by-Step Practical Tutorials & Operator Handbook

**Document Version:** 2.0.0  
**Target Audience:** Beginners, End Users, Project Reviewers, System Administrators  
**Notice:** All examples use safe, fictional company data (`Acme Global Technologies`, `Alex Chen`, `Sarah Jenkins`, `Priya Sharma`, `Elena Rostova`). Never input real production credentials into tutorials.

---

## Tutorial Catalog
1. [Tutorial 1: First-Time Application Setup & Navigation](#tutorial-1-first-time-application-setup--navigation)
2. [Tutorial 2: Processing a Meeting from Upload to Dossier](#tutorial-2-processing-a-meeting-from-upload-to-dossier)
3. [Tutorial 3: Inspecting & Verifying AI Intelligence](#tutorial-3-inspecting--verifying-ai-intelligence)
4. [Tutorial 4: End-to-End Task & Commitment Management](#tutorial-4-end-to-end-task--commitment-management)
5. [Tutorial 5: Projects & Strategic Decision Tracing](#tutorial-5-projects--strategic-decision-tracing)
6. [Tutorial 6: Organizational Knowledge Search & Grounded Ask AI](#tutorial-6-organizational-knowledge-search--grounded-ask-ai)
7. [Tutorial 7: Automated Calendar Synchronization & Job Queues](#tutorial-7-automated-calendar-synchronization--job-queues)
8. [Tutorial 8: Managing Third-Party SaaS Integrations (Google, Zoom, Email)](#tutorial-8-managing-third-party-saas-integrations-google-zoom-email)
9. [Tutorial 9: Team Administration, Audit Compliance & Quality Benchmarking](#tutorial-9-team-administration-audit-compliance--quality-benchmarking)
10. [Tutorial 10: System Troubleshooting & Disaster Recovery Runbook](#tutorial-10-system-troubleshooting--disaster-recovery-runbook)

---

# Tutorial 1: First-Time Application Setup & Navigation

### Objective
Start the MeetIntel AI services, authenticate as a team lead, verify system health, and understand the main workspace navigation.

### Prerequisites
- Python 3.10+ installed.
- Terminal access to the repository directory.

### Step-by-Step Instructions

#### 1. Launch the Application
Open your terminal in the project directory and start the Streamlit frontend:
```bash
.venv/bin/streamlit run app.py
```
*Why this matters:* Starts the web server on local port 8501 and initializes the database.  
*Expected Result:* Terminal displays:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

#### 2. Open the Browser & Sign In
Open `http://localhost:8501` in Chrome, Safari, or Firefox.
1. In the login box on the right panel, enter:
   - **Username:** `admin`
   - **Password:** `admin123` (or your seeded password).
2. Click the purple **Sign in** button.
*Why this matters:* Establishes a session token with administrative governance privileges.  
*Expected Result:* The login screen clears, and you land on the **Overview Dashboard** with the greeting *"Good morning/afternoon, Admin"*.

#### 3. Inspect System Status
1. In the left sidebar, scroll down to the **Governance** section.
2. Click **Preferences & Settings**.
3. Scroll to the bottom container titled **💻 System Architecture & Runtime Status**.
4. Verify that each core component shows operational:
   - *Database & Storage:* `SQLite (Local) / PostgreSQL Compatible`
   - *Vector Database:* `ChromaDB (Isolated Tenant Chunks)`
   - *Speech Engine:* `Faster-Whisper (CTranslate2)`
   - *Security & Encryption:* `Fernet 32-byte AES at rest`
*Expected Result:* All services show green operational status.

#### 4. Seed Demonstration Data (Recommended for First-Time Users)
1. On the same **Settings** page, locate the **🚀 Seed Examiner Demonstration Scenario** container.
2. Click the purple button: **✦ Seed Enterprise Demonstration Scenario**.
3. Wait 2 seconds.
*Why this matters:* Instantly generates realistic meetings, transcripts, decisions, and tasks so you can explore the application without needing to record an actual meeting first.  
*Expected Result:* A green notification appears: *"Successfully seeded enterprise demonstration data! Meeting #demo-meeting-q3-security created..."*

---

# Tutorial 2: Processing a Meeting from Upload to Dossier

### Objective
Take a safe test audio recording, upload it through the validation gate, monitor the 5-step AI pipeline, and view the generated meeting dossier.

### Prerequisites
- An audio file (you can use the included test file `test_meeting.wav` in the repository).
- Logged in as any user.

### Step-by-Step Instructions

#### 1. Navigate to Ingestion
Click **Process Meeting** in the sidebar (or click **＋ Process New Meeting** on the Overview dashboard).

#### 2. Select the Audio File
1. Make sure the **📁 Direct File Upload** tab is active.
2. Drag and drop `test_meeting.wav` into the upload box (or click **Browse files** and select it).
*Why this matters:* Ingests the raw audio into `data/uploads/` and validates that the audio container is not corrupted.  
*Expected Result:* A validation check runs. The page refreshes to reveal the **File Verification Screen**:
- Filename: `test_meeting.wav`
- Format: `WAV`
- Status badge: `Validated & Ready`

#### 3. Launch AI Processing
Click the purple button: **▶ Start AI Processing**.
*Why this matters:* Starts the 5-stage speech and intelligence pipeline.

#### 4. Observe the Live Processing Steps
Watch the real-time progress bar:
- **1/5 • Audio extraction (10%):** Volume normalization and 16kHz conversion.
- **2/5 • Transcription (30%):** Faster-Whisper transcribing speech turns.
- **3/5 • Speaker identification (60%):** Pyannote mapping speaker voices.
- **4/5 • AI analysis (90%):** LLM extracting summaries, decisions, and action items.
- **5/5 • Knowledge indexing (95%):** Embedding dialogue into ChromaDB vector store.
*Expected Result:* The progress bar reaches 100%, displays *"Processing complete!"*, and automatically redirects you to the **Meeting Results Dossier**.

---

# Tutorial 3: Inspecting & Verifying AI Intelligence

### Objective
Review AI-generated summaries, verify action items against verbatim transcripts, and ensure no hallucinated tasks enter the system.

### Prerequisites
- A processed meeting (e.g., `Q3 Architecture & Security Alignment`).

### Step-by-Step Instructions

#### 1. Review the Strategic Overview
1. Open the meeting dossier and select the **Overview** tab.
2. Read the **Executive Summary** to understand the high-level meeting outcome.
3. Check the **Risks and Dependencies** section. Note any flagged risks (e.g., *"Database latency spike during peak loads"* with severity `High`).

#### 2. Verify Action Items with Verbatim Quotes
1. Click the **Action Items** tab.
2. Find Task #1: *"Complete OAuth 2.0 PKCE integration"*.
3. Look directly underneath the title at the **Source Evidence Box**.
4. Verify the exact sentence quoted from the transcript:
   > *"Alex Chen: I will complete the OAuth 2.0 PKCE integration by this Friday."*
*Why this matters:* Guarantees that the task is real and that the AI did not hallucinate a commitment.

#### 3. Inspect Attributed Deadlines
1. Click the **Deadlines** tab.
2. Confirm that the confirmed date (`Friday, October 24th`) is linked to the deliverable.

#### 4. Audit Speaker Turn-by-Turn Dialogue
1. Click the **Transcript** tab.
2. In the **Search Transcript Dialogue** box, type `PKCE`.
*Expected Result:* The transcript instantly filters down to the exact dialogue turn where Alex committed to the deliverable with timestamp `[00:00:36]`.

---

# Tutorial 4: End-to-End Task & Commitment Management

### Objective
Update task progress as an employee, resolve blockers, and approve deliverables as a team lead.

### Prerequisites
- Logged in with active tasks.

### Step-by-Step Instructions

#### 1. View Your Personal Queue
1. In the sidebar, click **My Commitments**.
2. Notice your scope says: *"Showing personal commitments assigned to you"*.
3. Inspect your active tasks under the **Active Tasks** tab.

#### 2. Update Progress Notes
1. On Task #1, click the **Execution Status** dropdown and select **In Progress**.
2. In the **Notes / Blockers** text box, type:
   `PKCE challenge verification implemented on auth controller. Unit tests passing.`
3. Click the purple **Update** button.
*Why this matters:* Persists progress notes to the database and records an immutable audit log entry.  
*Expected Result:* A toast appears: *"Task #1 updated!"*. The progress note displays in a clean callout box.

#### 3. Flag an Active Blocker
1. If work is halted, change the status dropdown to **Blocked**.
2. In the notes box, type: `Waiting for DevOps to provision staging database replica.`
3. Click **Update**.
*Expected Result:* The task immediately moves to the **Blocked & Overdue** tab with an amber/red warning badge.

#### 4. Leadership Sign-Off (Team Lead / Admin)
1. In **Settings**, use the **Fast Role Switcher** to switch to `Sarah Jenkins (Team Lead)`.
2. Return to **My Commitments**.
3. Toggle the scope radio button to: **Organization-wide All Commitments (Team Lead View)**.
4. On any pending task, click the **🛡️ Management Actions** expander.
5. Click **✓ Approve Task**.
*Expected Result:* Approval badge turns green `Approved`. If Google Calendar is linked, a background job is scheduled to sync the deadline.

#### 5. Complete a Deliverable
1. When work is finished, select **Completed** from the status dropdown.
2. Click **Update**.
*Expected Result:* The task moves to the **Completed Deliverables** tab.

---

# Tutorial 5: Projects & Strategic Decision Tracing

### Objective
Link commitments to high-level corporate projects and track organizational decisions over time.

### Step-by-Step Instructions

#### 1. Open Strategic Projects
Click **Projects & Milestones** in the sidebar.

#### 2. Create a Strategic Project (Team Lead / Admin)
1. Click the expander: **＋ Register Strategic Project**.
2. Enter:
   - **Project Name:** `Enterprise Authentication Upgrade`
   - **Scope & Objectives:** `Migrate all customer-facing authentication to OAuth 2.0 with PKCE and audit logging.`
   - **Status:** `Active`
   - **Target Delivery Date:** 30 days from today.
3. Click **Save Strategic Initiative**.
*Expected Result:* A new project card appears showing 0% completed deliverables with target date countdown.

#### 3. Trace a Historical Decision
1. Click **Decision Register** in the sidebar.
2. In the search bar, type `OAuth`.
3. Locate Decision #1: *"Mandate OAuth 2.0 with PKCE for all client connections"*.
4. Inspect the card:
   - **Rationale:** Why was this chosen? (Eliminates credential interception vulnerabilities).
   - **Alternatives Considered:** What was rejected? (HTTP Basic Auth and static API tokens).
   - **Supporting Transcript Excerpt:** Verbatim quote from Sarah Jenkins.

#### 4. Revise / Supersede a Decision
1. On the decision card, open **⚙️ Supersede / Revise Decision**.
2. In the replacement text box, enter:
   `Mandate OAuth 2.0 with PKCE and require hardware security keys (FIDO2) for admin roles.`
3. Click **Confirm Revision & Mark Superseded**.
*Expected Result:* Original decision is marked `Superseded`. A new linked decision is registered as `Approved`. An entry is recorded in the Audit Trail.

---

# Tutorial 6: Organizational Knowledge Search & Grounded Ask AI

### Objective
Query across all meetings using semantic vector search and conversational RAG.

### Step-by-Step Instructions

#### 1. Open Knowledge Search
Click **Organizational Knowledge** in the sidebar.

#### 2. Ask a Cross-Meeting Question (Grounded RAG)
1. Ensure **✨ Grounded Ask AI** is selected.
2. In the chat box at the bottom, type:
   `What architectural decisions were made regarding authentication?`
3. Press **Enter**.
*Why this matters:* ChromaDB searches across thousands of transcript segments, extracts the top 5 relevant turns, and feeds them into Gemini/OpenAI to generate a factual answer.  
*Expected Result:* The AI replies:
> *"The engineering team decided to mandate OAuth 2.0 with PKCE for all client applications to prevent credential interception. Additionally, audit logs will be retained for 90 days."*
Underneath the answer, source pills appear: `✦ Q3 Architecture & Security Alignment`.

#### 3. Perform Direct Semantic Search
1. Click the button: **🔎 Semantic Direct Search**.
2. In the search input, type: `database connection pooling`.
3. Press **Enter**.
*Expected Result:* Renders ranked cards showing dialogue segments where database connection limits (e.g. "50 connections") were discussed, along with timestamp and speaker name.

---

# Tutorial 7: Automated Calendar Synchronization & Job Queues

### Objective
Verify that approving a task schedules a Google Calendar event and monitor background worker retries.

### Step-by-Step Instructions

#### 1. Check Integration Status
1. Navigate to **Integrations Center**.
2. Locate the **Google Calendar** card.
3. Ensure status displays `Connected — Live` or `Connected — Demo`. (If disconnected, click **Connect** to connect in demo mode).

#### 2. Trigger a Calendar Sync
1. Navigate to **Meeting Library** -> Open `Q3 Architecture & Security Alignment` -> **Action Items** tab.
2. Locate an unapproved task with a deadline.
3. Open **Management Actions** and click **✓ Approve Task**.
*Why this matters:* Triggers `GoogleWorkspaceIntegration.sync_task_to_calendar()`, generating an idempotency key `cal_sync_{task_id}` and scheduling a calendar reminder.  
*Expected Result:* Task card metadata updates to display green badge: `✓ Synced`.

#### 3. Inspect the Background Job Queue
1. In the sidebar, click **Workflow Automations**.
2. Select the **📜 Persistent Job Queue Log** tab.
3. Look at the top row:
   - Job Type: `[calendar_sync]`
   - Status: `COMPLETED` (or `QUEUED`)
   - Retries: `0/3`

#### 4. Run Worker Batch Manually
1. Click the button: **⚡ Run Worker Batch Now**.
*Expected Result:* A toast message reports: *"Worker processed N background job(s)!"*.

---

# Tutorial 8: Managing Third-Party SaaS Integrations (Google, Zoom, Email)

### Objective
Configure, test, and safely operate external integrations.

### Step-by-Step Instructions

#### 1. Test External Connection
1. Navigate to **Integrations Center**.
2. On the **Google Workspace** card, click **Test Connection**.
*Expected Result:* A green notification appears: *"Google Workspace connection operational"*.

#### 2. Generate Absent Employee Follow-up
1. Click **Calendar & Follow-ups** in the sidebar.
2. Under **Prepare Follow-up Draft**:
   - Meeting Source: `Q3 Architecture & Security Alignment`
   - Absent Team Member: `Elena Rostova`
3. Click **✦ Draft Personalized Follow-up**.
*Expected Result:* A draft email appears in the preview box addressed to Elena, summarizing the decisions and stating her assigned tasks.

#### 3. Approve and Dispatch Follow-up
1. Review the draft text.
2. Click **🚀 Approve & Dispatch Email**.
*Why this matters:* Enforces human-in-the-loop review before sending emails.  
*Expected Result:* Status changes to `Sent`, and an entry is logged in the **Delivery & Acknowledgment Log**.

---

# Tutorial 9: Team Administration, Audit Compliance & Quality Benchmarking

### Objective
Inspect team accountability rosters, run reproducible AI benchmarks, and export audit trails.

### Step-by-Step Instructions

#### 1. Inspect Team Directory (Admin / Lead Only)
1. In the sidebar under **Governance**, click **Team Directory**.
2. Review the member roster:
   - `Sarah Jenkins` (Team Lead, Engineering) — 1 Active • 2 Done
   - `Alex Chen` (Employee, Engineering) — 1 Active • 1 Done • ⚠️ 1 Blocked
   - `Priya Sharma` (Employee, QA) — 1 Active • 1 Done

#### 2. Run Reproducible AI Benchmarks
1. In the sidebar, click **AI Quality & Benchmarks**.
2. Click **✦ Run Reproducible AI Benchmark Evaluation**.
*Expected Result:* Within 1 second, the benchmark runner evaluates test datasets and renders:
- Transcription WER: `0.04` (Accuracy: `96.0%`)
- Action Item F1: `0.94` (Precision: `0.95`, Recall: `0.93`)
- Owner Accuracy: `100%`
- Evidence Grounding: `100%`
- Prompt Injection Defense: `100% Passed`

#### 3. Export Compliance Audit Log
1. Click **Audit Trail & Logs** in the sidebar.
2. Scroll to the bottom and click **↓ Export Audit Trail (CSV)**.
*Expected Result:* Downloads `Compliance_Audit_Trail.csv` to your computer containing timestamped records of every approval, status change, and user login.

---

# Tutorial 10: System Troubleshooting & Disaster Recovery Runbook

### Scenario A: Forgotten Administrator Password
- **Symptom:** You cannot log in with `admin` credentials.
- **Fix:** Run the command-line admin recovery utility:
  ```bash
  PYTHONPATH=. .venv/bin/python scripts/admin_recovery.py --username admin --password "NewSecurePassword123"
  ```
- **Result:** Directly hashes the new password with PBKDF2 salt, updates `meetintel.db`, and logs an audit recovery event.

### Scenario B: AI Rate Limit or Quota Exhaustion (HTTP 429)
- **Symptom:** LLM analysis fails with "Resource exhausted" or rate limit errors.
- **Fix:**
  1. MeetIntel AI's Provider Manager automatically marks Gemini unhealthy and switches to OpenAI.
  2. If both APIs are exhausted, open **Settings**, set **Primary AI Provider** to `Demo (Local Offline)`, and click **Save All Settings**.
  3. The application will continue operating offline using local heuristics.

### Scenario C: Faster-Whisper Model Download Hangs
- **Symptom:** The pipeline hangs at Step 2/5 (*Transcription*).
- **Cause:** Slow or blocked internet connection downloading model weights from Hugging Face.
- **Fix:** In **Settings**, change Whisper model to `base` (only ~140MB compared to ~500MB for `small`) and click **Save All Settings**.

### Scenario D: Database Locked Error (SQLite)
- **Symptom:** UI displays *"database is locked"*.
- **Cause:** Multiple concurrent write processes or an unclosed database session.
- **Fix:** MeetIntel AI automatically enables SQLite Write-Ahead Logging (`WAL`). Restart Streamlit to clear any hanging locks:
  ```bash
  pkill -f streamlit && .venv/bin/streamlit run app.py
  ```
