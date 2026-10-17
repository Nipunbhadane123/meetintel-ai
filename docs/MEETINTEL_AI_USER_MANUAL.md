# MeetIntel AI — Comprehensive User Manual & Beginner-Friendly Learning Guide

---

## Table of Contents
1. [Introduction to MeetIntel AI](#1-introduction-to-meetintel-ai)
   - [What is MeetIntel AI?](#what-is-meetintel-ai)
   - [What Problem Does It Solve?](#what-problem-does-it-solve)
   - [Who Uses MeetIntel AI?](#who-uses-meetintel-ai)
   - [Transcription vs. Intelligence vs. Execution](#transcription-vs-intelligence-vs-execution)
   - [Walkthrough: How a Meeting Becomes Work](#walkthrough-how-a-meeting-becomes-work)
   - [Beginner's Glossary of Terms](#beginners-glossary-of-terms)
2. [Getting Started & Authentication](#2-getting-started--authentication)
   - [Logging In & Self-Registration](#logging-in--self-registration)
   - [Understanding Roles and Permissions](#understanding-roles-and-permissions)
   - [Understanding Workspace Layout](#understanding-workspace-layout)
3. [Workspace Guide](#3-workspace-guide)
   - [Overview (Dashboard)](#31-overview-dashboard)
   - [My Commitments (Task Execution)](#32-my-commitments-task-execution)
   - [Meeting Library](#33-meeting-library)
   - [Process New Meeting (Ingestion & Processing Pipeline)](#34-process-new-meeting-ingestion--processing-pipeline)
   - [Meeting Results Dossier (The 8 Tabs Explained)](#35-meeting-results-dossier-the-8-tabs-explained)
4. [Planning & Intelligence Guide](#4-planning--intelligence-guide)
   - [Projects & Strategic Milestones](#41-projects--strategic-milestones)
   - [Decision Register](#42-decision-register)
   - [Pre-Meeting Preparation & Briefing](#43-pre-meeting-preparation--briefing)
   - [Organizational Knowledge Search & Grounded Ask AI](#44-organizational-knowledge-search--grounded-ask-ai)
5. [Automation & Ecosystem Guide](#5-automation--ecosystem-guide)
   - [Calendar & Attendance-Aware Follow-ups](#51-calendar--attendance-aware-follow-ups)
   - [Workflow Automations & Background Engine](#52-workflow-automations--background-engine)
   - [Enterprise Integration Center (Google, Zoom, Email)](#53-enterprise-integration-center-google-zoom-email)
6. [Governance & Administration Guide](#6-governance--administration-guide)
   - [Team Directory & Accountability](#61-team-directory--accountability)
   - [AI Quality Center & Benchmarks](#62-ai-quality-center--benchmarks)
   - [Compliance & System Audit Trail](#63-compliance--system-audit-trail)
   - [Preferences & System Administration](#64-preferences--system-administration)
7. [Specialized Views](#7-specialized-views)
   - [Transcript Library](#71-transcript-library)

---

# 1. Introduction to MeetIntel AI

### What is MeetIntel AI?
**MeetIntel AI** is an enterprise-grade **Meeting-to-Execution Intelligence Platform**. It does not simply record voice or turn spoken words into a wall of text. Instead, MeetIntel AI listens to workplace meetings (from audio files, video recordings, Zoom, or Google Meet), understands what was agreed upon, extracts concrete tasks and strategic decisions, and connects those outcomes directly into day-to-day work systems like Google Calendar, follow-up emails, and audit-logged project trackers.

### What Problem Does It Solve?
In most companies, meetings suffer from the **"Post-Meeting Amnesia Trap"**:
1. **Lost Action Items:** People verbally agree: *"I'll send the updated pricing proposal by Thursday"*, but nobody writes it down. Days later, nobody remembers who owned the task or when it was due.
2. **Endless Re-debating of Decisions:** A team debates an architectural choice for 45 minutes and reaches consensus. Three weeks later, someone who missed the meeting re-opens the exact same debate because there is no official, searchable record of *why* the decision was made or *what alternatives* were rejected.
3. **Punishing Absent Team Members:** If an employee is on leave, sick, or at a client site during a meeting, they are expected to read through a 20-page raw transcript or watch a 60-minute video just to find out if they were assigned a task.
4. **Lack of Accountability:** When tasks do get written down, they lack context. Team leads cannot verify whether an AI hallucinated an action item or whether an employee truly committed to it.

MeetIntel AI solves this by establishing a **single, verifiable source of truth** grounded in verbatim audio dialogue, combined with strict human-in-the-loop approvals.

### Who Uses MeetIntel AI?
MeetIntel AI is designed around three primary workplace roles:
1. **Employees / Contributors (e.g., Alex Chen, Priya Sharma):**
   - See their personal commitments clearly in one personal queue.
   - Update deliverable progress and flag blockers.
   - Automatically receive personalized email briefs if they miss a session.
2. **Team Leads / Managers (e.g., Sarah Jenkins):**
   - Review AI-suggested action items before they become official commitments.
   - Approve, reject, or reassign tasks.
   - Automatically push deadlines to employee Google Calendars.
   - Track team delivery velocity without micromanagement.
3. **Organization Administrators & Auditors (e.g., Admin User):**
   - Maintain security, API keys, and multi-tenant isolation.
   - Review immutable compliance audit logs showing who approved or altered any task.
   - Inspect measured AI accuracy benchmarks (Word Error Rate, F1 extraction score).

---

### Transcription vs. Intelligence vs. Execution

Understanding the difference between these three tiers is essential:

```
[ Level 1: Speech Transcription ]
Converts audio waveforms into raw text words.
Example: "Alex said I will finish the oauth pkce by friday."
Problem: Unstructured text. Nobody is assigned, no deadline is scheduled.
            │
            ▼
[ Level 2: Meeting Intelligence ]
AI reads transcript and extracts structured meaning.
Example: Task: "Complete OAuth 2.0 PKCE integration" | Owner: Alex Chen | Deadline: Friday | Confidence: 99%
Problem: Passive intelligence. It sits on a page without creating calendar events or tracking work.
            │
            ▼
[ Level 3: Meeting-to-Execution (MeetIntel AI) ]
Active enterprise workflow.
1. Team Lead verifies evidence quote and clicks [Approve Task].
2. Google Calendar event is automatically scheduled with reminders.
3. If Alex is blocked, downstream tasks flag risk warnings automatically.
4. If Elena missed the meeting, an approved email brief is queued for dispatch.
5. All actions are immutably recorded in the compliance audit trail.
```

---

### Walkthrough: How a Meeting Becomes Work

Here is a realistic scenario illustrating MeetIntel AI in action:

1. **The Meeting:** The Acme Global engineering team holds a 30-minute review on Google Meet.
   - *Sarah Jenkins (Lead):* "We need to complete our OAuth 2.0 PKCE upgrade before Q3 audit."
   - *Alex Chen (Engineer):* "I will take that. I'll complete the PKCE integration by Friday, October 24th."
   - *Sarah:* "Agreed. Elena is out today at a customer site, so let's make sure she gets a follow-up."
2. **Upload & Processing:** The recording (`Q3_Architecture_and_Security.wav`) is uploaded to MeetIntel AI.
3. **Automated Pipeline:**
   - **FFmpeg** standardizes audio to 16kHz mono WAV.
   - **Faster-Whisper** transcribes dialogue turns with timestamps.
   - **Pyannote Audio** diarizes speaker voices.
   - **Gemini / OpenAI** extracts the executive summary, decisions, and action items with verbatim evidence quotes.
   - **ChromaDB** indexes the dialogue into searchable vector embeddings.
4. **Human-in-the-Loop Review:** Sarah Jenkins opens **My Commitments** or the meeting's **Action Items** tab. She sees the suggested task: *"Complete OAuth 2.0 PKCE integration"*. She verifies the quote: *"Alex Chen: I will complete the OAuth 2.0 PKCE integration by this Friday."* She clicks **Approve Task**.
5. **Automated Execution:**
   - Google Calendar receives an event: `[MeetIntel] Complete OAuth 2.0 PKCE integration` scheduled for Friday.
   - Alex Chen logs into his dashboard and sees the task at the top of his **"What Should I Do Next?"** queue.
   - Sarah opens **Calendar & Follow-ups** and clicks **Draft Personalized Follow-up**. MeetIntel AI drafts an email specifically for Elena Rostova containing only Sarah's approved decisions and tasks. Sarah reviews it and clicks **Approve & Dispatch**.
   - An immutable record is saved in the **Audit Trail**.

---

### Beginner's Glossary of Terms

| Term | Beginner-Friendly Definition |
| :--- | :--- |
| **Action Item** | A specific, measurable commitment extracted from dialogue (e.g., "Build OAuth endpoint") with an assigned owner, target deadline, and priority. |
| **Audit Trail** | An immutable (tamper-proof) history log recording every single action: who created a task, who approved it, who changed its status, and when. |
| **CTranslate2** | A high-performance inference engine that allows Faster-Whisper to run speech transcription locally on your computer fast without GPU cloud costs. |
| **Diarization (Speaker Diarization)** | The process of answering *"Who spoke when?"*. It separates different people's voices in a recording (Speaker 1 vs Speaker 2). |
| **Evidence Excerpt** | The verbatim sentence extracted directly from the transcript that proves why an AI created a task or decision. Prevents AI hallucinations. |
| **Faster-Whisper** | A reimplementation of OpenAI's Whisper speech-to-text model that is up to 4x faster and uses less memory while maintaining high accuracy. |
| **Fernet AES Cryptography** | Enterprise-grade 32-byte encryption standard used by MeetIntel AI to encrypt OAuth secrets and API tokens so they are safe in the database. |
| **Idempotency Key** | A unique code assigned to an event to prevent accidental duplicates. For example, if you click "Sync Calendar" twice, the key ensures only one calendar event is created. |
| **JiWER / WER** | **Word Error Rate**. The standard mathematical formula used by data scientists to measure speech transcription error. (A WER of 0.05 means 95% word accuracy). |
| **Minutes of Meeting (MoM)** | The official consolidated executive document summarizing participants, discussions, decisions, and tasks from a meeting. |
| **Multi-Tenant Isolation** | A security architecture ensuring that Organization A (e.g., Acme Global) can never see, search, or access meetings, vectors, or tasks from Organization B. |
| **PBKDF2** | Password-Based Key Derivation Function 2. A cryptographic standard that hashes passwords 100,000 times with random salt so they can never be reversed. |
| **RAG (Retrieval-Augmented Generation)** | An AI technique where the system first searches your private meeting transcripts for relevant facts, and then feeds those exact facts to the LLM to write an accurate answer. |
| **Vector Embedding** | Turning sentences into lists of numbers that represent their meaning. This allows you to search by *concept* (e.g., "budget cuts") even if the speaker said "reduced expenditure". |

---

# 2. Getting Started & Authentication

### Logging In & Self-Registration
When you launch MeetIntel AI, the application opens with an authentication screen:
- **Left Banner:** Visual overview of MeetIntel AI's value proposition (*Transcript -> Insights -> Decisions -> Action Items*).
- **Right Panel:** Two tabs: **Login** and **Create Account**.

#### How to Sign In:
1. Select the **Login** tab.
2. Enter your **Username** (e.g., `admin`, `sarah_lead`, `alex_eng`, or `priya_qa`).
3. Enter your **Password** (e.g., `admin123` or your personal password).
4. Click **Sign in**.
5. *Result:* MeetIntel AI authenticates your password using PBKDF2 verification, records a `LOGIN` event in the Audit Trail, loads your workspace session, and directs you to the **Overview Dashboard**.

#### How to Register a New Account:
1. Select the **Create Account** tab.
2. Choose a unique **Username** (letters, numbers, underscores).
3. Enter your corporate **Email** (e.g., `yourname@acmeglobal.io`).
4. Enter and confirm your **Password** (minimum 6 characters recommended).
5. Click **Register**.
6. *Result:* Your account is created in the database, assigned to the default organization (`Acme Global`) with the role of `Employee`, and you can immediately log in.

---

### Understanding Roles and Permissions

MeetIntel AI enforces strict server-side Role-Based Access Control (RBAC):

| Role | Intended User | Permissions & Visible Pages |
| :--- | :--- | :--- |
| **Employee** | Software Engineers, Designers, QA, Analysts | **Can:** View Overview, My Commitments (personal view), Meeting Library, Meeting Dossiers, Knowledge Search, Transcripts, and Preferences.<br>**Can:** Update own task execution status (In Progress, Blocked, Completed) and add progress notes.<br>**Cannot:** Approve/reject/reassign tasks, dispatch emails, view Team Directory, view AI Quality benchmarks, or inspect full Audit Trail. |
| **Team Lead** | Engineering Managers, Project Managers, Scrum Masters | **All Employee permissions PLUS:**<br>**Can:** Toggle between personal and org-wide task views.<br>**Can:** Approve, reject, or reassign action items.<br>**Can:** Supersede and revise decisions.<br>**Can:** Generate and dispatch absent employee follow-up emails.<br>**Can:** Access Team Directory, AI Quality Center, and Audit Trail.<br>**Can:** Trigger manual background worker batches. |
| **Admin** | System Administrators, IT Leads | **All Team Lead permissions PLUS:**<br>**Can:** Configure API keys (Gemini, OpenAI, Hugging Face, Whisper model) in Settings.<br>**Can:** Connect and disconnect SaaS integrations (Google Workspace, Zoom, SMTP).<br>**Can:** Execute administrative account recovery and database seeding tools. |

---

### Understanding Workspace Layout

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ✦ MeetIntel AI                                                         Workspace       │
│ Meeting-to-Execution                                                  [Acme Global]    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ WORKSPACE                                                                              │
│  ⊞ Overview (Dashboard)                                                                │
│  ☑ My Commitments (My Tasks)                                                           │
│  🎙 Meeting Library                                                                    │
│  ＋ Process Meeting                                                                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ PLANNING & INTELLIGENCE                                                                │
│  ⚑ Projects & Milestones                                                               │
│  ⚖ Decision Register                                                                   │
│  ◷ Meeting Preparation                                                                 │
│  ✦ Organizational Knowledge                                                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ AUTOMATION & ECOSYSTEM                                                                 │
│  ✉ Calendar & Follow-ups                                                               │
│  ⚡ Workflow Automations                                                                │
│  🔌 Integrations Center                                                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GOVERNANCE (Admins & Leads)                                                            │
│  👥 Team Directory                                                                     │
│  📈 AI Quality & Benchmarks                                                            │
│  🛡 Audit Trail & Logs                                                                 │
│  ⚙ Preferences & Settings                                                              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [User Avatar] Sarah Jenkins (@sarah_lead)                                 [Log out]    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

The sidebar provides consistent navigation. When a page is active, its button is highlighted with the primary brand style. At the bottom, your profile card displays your avatar initial, full name, username, and a one-click **Log out** button.

---

# 3. Workspace Guide

## 3.1 Overview (Dashboard)

### A. What is this page?
The **Overview Dashboard** is the command center of MeetIntel AI. It gives you an immediate operational snapshot of your personal work, urgent deadlines, and recent meeting intelligence.

### B. Why do we need it?
Without a centralized dashboard, employees waste time clicking across multiple tools to see what tasks they owe, what blockers exist, or what happened in today's meetings. The dashboard answers three critical questions in under 5 seconds:
1. *What should I work on right now?*
2. *What deadlines are approaching across the team?*
3. *What blockers or governance items need attention?*

### C. When should I use it?
- Every morning when starting your workday.
- Immediately after logging into the system.
- To quickly launch a new meeting ingestion or check session processing status.

### D. How do I open it?
Click **Overview** in the sidebar under the **Workspace** category.

### E. How do I use it?
1. Check the **Top Metric Cards** to see your total commitments and active blockers.
2. Review **"1. What Should I Do Next?"** to see your immediate deliverable. Click **View My Commitments →** to jump straight to work.
3. Review **"2. What Is Due Soon?"** to see upcoming team deadlines.
4. Review **"3. What Needs My Attention?"** to see if any tasks are blocked or awaiting approval.
5. Review **"4. Recent Meeting Dossiers"** and click **View Dossier →** on any card to view full transcripts and summaries.

### F. Interface Breakdown
- **Executive Header:** Shows organization name (`Acme Global`), today's formatted date, your role badge (`Admin`, `Team Lead`, or `Employee`), greeting (`Good morning/afternoon/evening, Name`), and a primary **＋ Process New Meeting** button.
- **Metric Card 1 — My Commitments:** Total tasks assigned to you in this workspace, with a caption showing how many are active.
- **Metric Card 2 — Pending Approvals:** Total action items across the organization awaiting leadership sign-off.
- **Metric Card 3 — Blockers & Risks:** Total deliverables currently marked `Blocked` by dependencies.
- **Metric Card 4 — Sessions Processed:** Cumulative count of meetings ingested and analyzed in the organization.
- **Card: What Should I Do Next? (Personal Queue):**
  - Renders task title, description, target deadline, priority level, estimated effort hours, and a direct navigation button.
  - If you have no pending tasks, renders a clean green checkmark: *"All Commitments Clear"*.
- **Card: What Is Due Soon? (Organization-Wide):**
  - Lists the next 3 upcoming uncompleted deliverables with assignee name, execution status, and deadline date.
- **Card: What Needs My Attention? (Risks & Governance):**
  - Displays alert rows for blocked tasks, pending approvals, and unassigned tasks requiring leadership input.
- **Card: Recent Meeting Dossiers:**
  - Displays up to 3 cards with meeting title, date, duration, speaker count, platform source icon (Google Meet, Zoom, or Audio Upload), and status badge.

### G. Practical Example
> **Scenario:** Alex Chen logs in on Monday morning.
> - Greeting reads: *"Good morning, Alex Chen"*.
> - Metric card shows *2 Active Commitments*.
> - Personal queue highlights: *"Complete OAuth 2.0 PKCE integration"*, Priority: `High`, Deadline: `Friday, October 24th`, Effort: `8.0h`.
> - Alex clicks **View My Commitments →** and immediately begins work without searching through emails or notes.

### H. Common Mistakes & Troubleshooting
- **Metric counts show 0:** If you just installed the application, the database is empty. Go to **Settings** and click **Seed Enterprise Demonstration Scenario** to instantly populate realistic data.
- **Process button does nothing:** The button redirects to the "New Meeting" page; ensure you are not navigating back via browser history.

---

## 3.2 My Commitments (Task Execution)

### A. What is this page?
The **My Commitments** page is the personal accountability and execution workspace. It tracks every task assigned to you from meeting conversations, lets you update your progress, flag dependencies, and review the exact evidence quotes behind each deliverable.

### B. Why do we need it?
Task management in ordinary tools often separates the *task* from the *context*. When an engineer asks: *"Why am I doing this?"*, they have to dig through old chat logs. MeetIntel AI attaches the **verbatim transcript quote** to every single task card, making assignments transparent and undeniable.

### C. When should I use it?
- When working on your deliverables.
- When you finish a task and want to mark it `Completed`.
- When you are waiting on someone else and need to mark a task `Blocked`.
- (For Leads) When reviewing new action items to approve or reassign them.

### D. How do I open it?
Click **My Commitments** in the sidebar under **Workspace**.

### E. How do I use it?
1. **Choose your scope (Leads/Admins only):** Use the radio button at the top to toggle between *"My Personal Commitments"* and *"Organization-wide All Commitments"*.
2. **Select a tab:**
   - **Active Tasks:** Work that is currently underway or pending.
   - **Blocked & Overdue:** Items needing immediate intervention.
   - **Completed Deliverables:** Finished work history.
   - **Audit Trail:** Step-by-step compliance log of every status update.
3. **Update progress:**
   - On any task card, choose a new status from the **Execution Status** dropdown (`In Progress`, `Blocked`, `Completed`, etc.).
   - Type progress details or dependency blockers in the **Notes / Blockers** input field.
   - Click the purple **Update** button.
4. **Approve a task (Team Leads/Admins):**
   - Click the **Management Actions** expander on any card.
   - Click **✓ Approve Task**. (This automatically triggers calendar sync!).
5. **Reassign a task (Team Leads/Admins):**
   - In the **Management Actions** expander, select another team member from the dropdown and click **Reassign Task**.

### F. Interface Breakdown
- **Task Header:** Task title, descriptive summary, and dual status badges (Approval Status: `Draft`/`Approved`/`Rejected` and Execution Status: `Pending`/`In Progress`/`Blocked`/`Completed`).
- **Source Evidence Box:** A light purple callout box showing the verbatim quote from the meeting transcript and meeting title.
- **Metadata Grid:** 5 clean columns showing Assignee, Target Deadline, Priority (color-coded red if High/Urgent), Estimated Effort Hours, and Calendar Sync status pill.
- **Progress Notes Banner:** Displays the latest comment or blocker explanation entered by the assignee.
- **Interactive Control Bar:** Dropdown selector (`Draft`, `Pending`, `Approved`, `Scheduled`, `In Progress`, `Blocked`, `Completed`), text input for notes, and an **Update** button.
- **Management Expander (Admin/Lead only):** Contains **✓ Approve Task**, rejection button, and reassignment user selector.
- **Task Audit Expander:** Shows the complete historical changelog for this specific task.

### G. Practical Example
> **Scenario:** Alex Chen is working on the OAuth integration. The staging database replica goes down.
> 1. Alex opens **My Commitments** -> **Active Tasks**.
> 2. On Task #1 (*Complete OAuth 2.0 PKCE integration*), he changes status from `In Progress` to `Blocked`.
> 3. In the notes field, he types: *"Blocked on staging database replica provision by DevOps team."*
> 4. Alex clicks **Update**.
> 5. *Result:* The task immediately moves to the **Blocked & Overdue** tab. A warning indicator appears on Sarah Jenkins's overview dashboard, alerting her to resolve the blocker.

---

## 3.3 Meeting Library

### A. What is this page?
The **Meeting Library** is the centralized repository of all meetings ingested and analyzed by MeetIntel AI across your organization.

### B. Why do we need it?
Teams have dozens of meetings every month. The Library allows you to find any past meeting instantly by typing a keyword, filtering by status, or sorting by date, without needing to remember exact file names or dates.

### C. When should I use it?
- When you want to revisit the dossier of a previous session.
- When searching for a meeting where a specific topic (e.g., "pricing", "database migration") was discussed.
- To check whether a newly uploaded recording has finished processing.

### D. How do I open it?
Click **Meeting Library** in the sidebar under **Workspace**.

### E. How do I use it?
1. In the **Search Library** bar, type any word (e.g., `security`, `sprint`, `architecture`). The list filters instantly.
2. Use the **Status Filter** dropdown to view only `Completed`, `Processing`, or `Failed` meetings.
3. Use the **Sort By** dropdown to order by `Newest Date`, `Oldest Date`, `Duration (Longest)`, or `Title (A-Z)`.
4. Click **View Dossier →** on any meeting card to open its full 8-tab intelligence dossier.

### F. Interface Breakdown
- **Search & Filter Bar:** 3 unboxed controls: text input, status dropdown, and sort dropdown.
- **Results Counter:** Shows e.g., *"Showing 4 of 4 recorded sessions"*.
- **Meeting Cards:**
  - **Source Pill:** Indicates `Google Meet`, `Zoom`, or `Audio Upload`.
  - **Title:** Full meeting title (e.g., `Q3 Architecture & Security Alignment`).
  - **Metadata Row:** Date, formatted duration (e.g., `30m 40s`), and number of detected speakers.
  - **Summary Excerpt:** Two-line preview of the executive summary.
  - **Status Badge:** `Completed`, `Processing`, or `Failed`.
  - **Action Button:** Purple **View Dossier →** button.

---

## 3.4 Process New Meeting (Ingestion & Processing Pipeline)

### A. What is this page?
The **Process New Meeting** page is the entry point for turning raw audio or video recordings into intelligence dossiers. It includes format validation, deduplication checks, and the live 5-step processing pipeline.

### B. Why do we need it?
Raw audio files are large, uncompressed, and messy. MeetIntel AI validates file integrity before running expensive AI models, protects against processing duplicate files twice, and provides real-time progress feedback.

### C. When should I use it?
Whenever you have a new meeting recording (from an in-person voice memo, Zoom cloud recording, or Google Meet video) that you want to analyze.

### D. How do I open it?
Click **Process Meeting** in the sidebar under **Workspace**, or click the **＋ Process New Meeting** button on the dashboard.

### E. How do I use it?
#### Step 1: Ingestion
You can ingest meetings via three tabs:
1. **Direct File Upload (Recommended):**
   - Drag and drop your audio or video file (`.wav`, `.mp3`, `.m4a`, `.mp4`, `.flac`, `.ogg`, `.mov`, `.mkv`, `.avi` up to 250 MB).
   - MeetIntel AI instantly validates the file format and checks its MD5 hash.
2. **Import from Zoom (Sandbox Mode):**
   - Enter a Zoom Meeting ID (e.g., `849 2014 9912`) and click **Import Recording** to test the pipeline using a reference sandbox file.
3. **Import from Google Meet:**
   - If Google Workspace is connected, click to discover recordings and `.vtt` transcripts stored in your linked Google Drive folder.

#### Step 2: Verification Screen
Once validated, MeetIntel AI displays a file card with:
- Filename, File Size (MB), Duration, and Audio Format.
- Status badge: `Validated & Ready` (or `Already Processed` if the file was previously ingested).
- Two buttons: **Cancel & Remove File** and **▶ Start AI Processing**.

#### Step 3: Starting the Pipeline
Click **▶ Start AI Processing**. The system navigates to the live pipeline screen:
- **Step 1/5 • Audio Extraction:** Normalizes volume and converts audio to 16kHz mono WAV via FFmpeg.
- **Step 2/5 • Transcription:** Executes Faster-Whisper with VAD to transcribe dialogue turns.
- **Step 3/5 • Speaker Identification:** Executes Pyannote to map speaker turns and aligns words with speakers.
- **Step 4/5 • AI Analysis:** Calls Gemini / OpenAI to extract executive summaries, structured decisions, and action items with evidence.
- **Step 5/5 • Knowledge Indexing:** Embeds the dialogue turns into ChromaDB vector store for semantic search.
- When finished, the system automatically redirects you to the **Meeting Results Dossier**.

### F. Troubleshooting Failed Uploads
- **"File format not supported":** Convert your file to standard MP3 or WAV, or ensure the file has a valid extension.
- **"This exact meeting audio has already been processed":** MeetIntel AI's MD5 deduplication detected that this file is already in your library. Click **▶ View Meeting Results** to see existing data without wasting AI tokens.

---

## 3.5 Meeting Results Dossier (The 8 Tabs Explained)

When you open a meeting from the library or complete processing, MeetIntel AI renders the comprehensive **Intelligence Dossier**.

### Header Section
- **Platform Source Tag:** `INTELLIGENCE DOSSIER • GOOGLE MEET / ZOOM / AUDIO UPLOAD`.
- **Title:** The full meeting title.
- **Metadata:** Formatted date, duration, speaker count, and status badge (`Completed`).
- **Navigation:** Purple button **← Back to Meeting Library** to return safely.

---

### Tab 1: Overview
- **Executive Summary:** A cohesive, narrative paragraph synthesizing what occurred in the meeting.
- **Meeting Objective & Emotional Analysis:** Two cards detailing the primary goal of the session and the emotional tone (e.g., *"Constructive, decisive, and focused"*).
- **Key Topics & Discussion Points:** Structured bulleted lists highlighting the main agenda subjects and arguments debated.
- **Recommendations & Next Steps:** Forward-looking strategic suggestions extracted by the AI.
- **Risks & Dependencies Table:** Color-coded warning callout detailing operational risks, severity impact (`High`/`Medium`), contextual explanation, and suggested mitigation steps.
- **Export (JSON):** Download raw structured JSON for external data pipelines.

---

### Tab 2: Action Items
- Displays every action item identified in this specific meeting.
- For each item, shows task title, description, assigned owner (with verification status), target deadline, priority level, estimated effort hours, and the verbatim transcript quote.
- Allows inline status updates and management approvals directly on the tab.
- Includes a **↓ Export Verified Action Items (CSV)** button.

---

### Tab 3: Participants
- Lists every speaker detected in the meeting with their assigned speaker ID (e.g., `Speaker 1`, `Speaker 2`) and resolved name.
- Displays an avatar initial pill for each participant.
- Shows a list of **Attributed Responsibilities** extracted from dialogue turns for each person.

---

### Tab 4: Deadlines
- Timeline view of confirmed milestone dates and commitments mentioned in the meeting.
- Each row links the date (e.g., `Friday, October 24th`) to its associated deliverable task.

---

### Tab 5: Priorities
- Urgency classifications assigned by the AI.
- Highlights items marked `High` or `Urgent` with color-coded badges to help teams allocate sprint resources effectively.

---

### Tab 6: Transcript
- **Dialogue Turns:** Turn-by-turn breakdown showing timestamp (e.g., `[00:01:15]`), speaker name, and spoken text.
- **Keyword Search:** Real-time filter box to find specific phrases in the transcript.
- **↓ Download TXT:** Downloads the complete verbatim transcript with timestamps.
- **Speech Recognition Accuracy Benchmark (WER Tool):**
  - An interactive evaluation expander.
  - Paste any reference "ground-truth" script into the text area and click **Evaluate Accuracy & WER**.
  - Calculates the exact mathematical Word Error Rate (WER) and Word Recognition Accuracy % using JiWER.

---

### Tab 7: Ask AI
- An interactive, conversational chatbot specifically scoped to **this meeting**.
- **How to use:** Type any question into the chat input (e.g., *"Did anyone object to the OAuth migration?"* or *"What did Alex say about the database?"*).
- **Output:** The AI synthesizes an answer and provides an expandable citation drawer showing the exact transcript excerpts it used to form the answer.

---

### Tab 8: MoM (Minutes of Meeting)
- Consolidates Executive Summary, Attendees, Discussion Points, Decisions, Action Items, and Recommendations into standard corporate MoM format.
- **Interactive Preview:** Clean, scrollable text preview of the entire Minutes of Meeting.
- **4 Export Formats:**
  1. **📄 Download PDF:** Generates a styled, branded corporate PDF report (`reports/pdf.py`) with DejaVu fonts.
  2. **📝 Download Word:** Generates a Microsoft Word (`.docx`) document formatted with official headers and bulleted tables (`reports/docx.py`).
  3. **📊 Download CSV:** Generates a tabular spreadsheet of deliverables (`reports/csv.py`).
  4. **📃 Download TXT:** Generates an ASCII plaintext file suitable for terminal logs or quick copy-pasting.

---

# 4. Planning & Intelligence Guide

## 4.1 Projects & Strategic Milestones

### A. What is this page?
The **Projects & Milestones** view groups meeting commitments and decisions under high-level corporate initiatives (e.g., *"Enterprise Security Architecture"*, *"Cloud Platform Migration"*).

### B. Why do we need it?
Meetings rarely exist in isolation. A single strategic project might span 10 meetings over 3 months. This page aggregates tasks and decisions across all those sessions into a single milestone progress view.

### C. When should I use it?
- During sprint planning or leadership reviews.
- To monitor deliverable completion velocity across initiatives.
- To check whether a project is on schedule to meet its target delivery date.

### D. How do I open it?
Click **Projects & Milestones** in the sidebar under **Planning & Intelligence**.

### E. How do I use it?
1. **Review Project Metrics:** The top cards show Active Initiatives, Delivered Outcomes, Open Deliverables, and At-Risk Items.
2. **Register a New Project (Admins/Leads):**
   - Expand the **＋ Register Strategic Project** accordion.
   - Enter **Project Name** (e.g., `SOC2 Compliance Preparation`).
   - Enter **Scope & Objectives**.
   - Select status (`Active`, `At Risk`, `Completed`, `On Hold`) and target delivery date.
   - Click **Save Strategic Initiative**.
3. **Seed Standard Initiatives:** If no projects exist, click **✦ Initialize Standard Strategic Initiatives** to populate default corporate tracks.
4. **Inspect Project Progress:** Each project card displays a progress bar (percentage of tasks completed), target date countdown, and active blockers count.

---

## 4.2 Decision Register

### A. What is this page?
The **Decision Register** is an immutable, searchable catalog of all official agreements made across your organization's meetings.

### B. Why do we need it?
Teams waste hundreds of hours re-litigating decisions because nobody recorded the *rationale* or the *alternatives* that were considered. The Decision Register preserves the context, evidence, and proposer for every agreement.

### C. When should I use it?
- When onboarding new employees who need to understand why systems are designed a certain way.
- Before proposing an architecture or process change.
- When an agreement needs to be officially superseded or revised.

### D. How do I open it?
Click **Decision Register** in the sidebar under **Planning & Intelligence**.

### E. How do I use it?
1. **Search & Filter:** Search by keywords (e.g., `OAuth`, `retention`) or filter by status (`Approved`, `Proposed`, `Superseded`, `Rejected`).
2. **Inspect Decision Details:** Each card reveals:
   - Agreement summary.
   - **Rationale & Context** (why this choice was made).
   - **Alternatives Considered** (what options were evaluated and rejected).
   - **Supporting Transcript Excerpt** (verbatim meeting dialogue).
   - Proposer name and source meeting.
3. **Supersede a Decision (Admins/Leads):**
   - On an approved decision, open the **⚙️ Supersede / Revise Decision** expander.
   - Type the new agreement replacing it.
   - Click **Confirm Revision & Mark Superseded**.
   - *Result:* The old decision status changes to `Superseded`, a new linked decision is created as `Approved`, and an immutable audit event is recorded.
4. **Export CSV:** Click **↓ Export Register (CSV)** at the bottom to download the complete decision log.

---

## 4.3 Pre-Meeting Preparation & Briefing

### A. What is this page?
The **Meeting Preparation** page generates proactive executive briefing dossiers before an upcoming meeting takes place.

### B. Why do we need it?
Most meetings start with 15 minutes of confusion: *"Who was supposed to do that?"*, *"Did we ever resolve that blocker?"*. Meeting Prep synthesizes past outcomes, unresolved action items, and active blockers so attendees arrive fully prepared.

### C. When should I use it?
- 15 to 30 minutes before stepping into a recurring sprint review, 1-on-1, or architecture session.
- When planning the agenda for an upcoming discussion.

### D. How do I open it?
Click **Meeting Preparation** in the sidebar under **Planning & Intelligence**.

### E. How do I use it?
1. In the **Baseline Previous Meeting** dropdown, select the past meeting you want to build upon.
2. In the **Upcoming Session Goal** input, enter the objective of the upcoming meeting (e.g., `Sprint Execution & Security Readiness Review`).
3. Click **✦ Generate Preparation Brief**.
4. Review the generated 5-part brief:
   - **Previous Session Synthesis:** Quick recap of past agreements.
   - **Known Blockers & Risks:** Red warning callouts of open dependencies.
   - **Outstanding Action Items:** Tasks from prior sessions that are still pending.
   - **Suggested Agenda:** Timed meeting agenda recommendations (e.g., 10m review, 15m blocker deep dive).
   - **Recommended Discussion Points:** Targeted questions for the team.

---

## 4.4 Organizational Knowledge Search & Grounded Ask AI

### A. What is this page?
The **Organizational Knowledge** page is an enterprise search engine and conversational AI assistant that queries across **every meeting ever held** in your workspace.

### B. Why do we need it?
Valuable institutional knowledge is buried inside recorded meetings. Rather than asking colleagues *"Did we ever discuss GDPR compliance?"*, you can search or ask the knowledge base directly.

### C. When should I use it?
- To find answers to cross-meeting technical questions.
- To locate specific meetings without knowing their titles.
- To verify past commitments across multiple quarters.

### D. How do I open it?
Click **Organizational Knowledge** in the sidebar under **Planning & Intelligence**.

### E. How do I use it?
You can toggle between two modes:
#### Mode 1: Grounded Ask AI (Conversational RAG)
1. Click **✨ Grounded Ask AI**.
2. Type any question into the chat input at the bottom (e.g., *"What decisions were made regarding the Q3 product roadmap?"* or *"Who is working on database pooling?"*).
3. The AI retrieves relevant chunks from ChromaDB, synthesizes a clear answer, and displays **source pills** underneath referencing the meetings it cited.

#### Mode 2: Semantic Direct Search
1. Click **🔎 Semantic Direct Search**.
2. Type keywords or natural language queries (e.g., `database latency`, `OAuth PKCE`).
3. View ranked match cards with similarity scores, meeting titles, dates, and preview snippets.

---

# 5. Automation & Ecosystem Guide

## 5.1 Calendar & Attendance-Aware Follow-ups

### A. What is this page?
The **Calendar & Follow-ups** page manages attendance-aware notifications and calendar reminders. It ensures team members who missed a meeting receive an approved follow-up summary and can acknowledge receipt of their tasks.

### B. Why do we need it?
Automated tools often spam absent employees with unverified transcripts. MeetIntel AI enforces **attendance awareness** (based on verified organizer records, never silence) and **human-in-the-loop email gating** (a manager must approve the draft before dispatch).

### C. When should I use it?
- Immediately after processing a meeting where a team member was absent or excused.
- To inspect delivery logs and verify whether an employee confirmed receipt of their tasks.

### D. How do I open it?
Click **Calendar & Follow-ups** in the sidebar under **Automation & Ecosystem**.

### E. How do I use it?
#### Tab 1: Prepare Follow-up Draft
1. Select the **Meeting Source** from the dropdown.
2. Select the **Absent Team Member** (e.g., `Elena Rostova`).
3. Click **✦ Draft Personalized Follow-up**.
4. Inspect the generated email preview. Notice that it contains only approved decisions and tasks relevant to that person.
5. (Admins/Leads) Click **🚀 Approve & Dispatch Email** to send it via SMTP (or log simulated dispatch in demo mode).

#### Tab 2: Delivery & Acknowledgment Log
1. Inspect the table of sent notifications.
2. If an employee logs in and views a notification sent to them, they can click **Confirm Acknowledgment & Accept Tasks**.
3. *Result:* The notification status updates to `Acknowledged`, and an immutable event is written to the audit log.

---

## 5.2 Workflow Automations & Background Engine

### A. What is this page?
The **Workflow Automations** page monitors event-driven automation rules and the persistent background job queue.

### B. Why do we need it?
Asynchronous tasks (calendar event creation, email dispatches, webhook ingestion) must run reliably without freezing the user interface. If a third-party server is temporarily slow, jobs must automatically retry with exponential backoff.

### C. When should I use it?
- To monitor active automation triggers.
- To inspect background queue health (Queue Depth, Jobs Executed, Dead-letter/Failed).
- To manually trigger an immediate queue run via **⚡ Run Worker Batch Now**.

### D. How do I open it?
Click **Workflow Automations** in the sidebar under **Automation & Ecosystem**.

### E. How do I use it?
- **Tab 1: Active Workflow Rules:** View rules such as *Auto-Schedule Approved Deadlines*, *Attendance-Aware Absentee Gating*, and *Dependency Blocker Escalation*.
- **Tab 2: Persistent Job Queue Log:** View recent background jobs with retry counts (`0/3`), scheduled execution times, and status badges (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`).
- **Run Worker Batch:** Click **⚡ Run Worker Batch Now** to immediately process all queued background jobs without waiting for the background polling loop.

---

## 5.3 Enterprise Integration Center (Google, Zoom, Email)

### A. What is this page?
The **Integrations Center** manages connections to external enterprise SaaS tools: **Google Workspace** (Google Calendar & Meet), **Zoom**, and **SMTP Email**.

### B. Why do we need it?
Organizations need to connect their conferencing tools and calendars securely. MeetIntel AI provides:
- **Verified Live Mode:** Real OAuth 2.0 and API keys for production environments.
- **Sandboxed Demo Mode:** Full simulated workflows for examiner evaluations without requiring paid enterprise SaaS subscriptions.
- **Fernet AES Encryption:** All tokens are encrypted at rest.

### C. When should I use it?
- During initial application setup.
- To verify whether external APIs are responding via **Test Connection**.
- To sync all approved task deadlines to Google Calendar in one click.

### D. How do I open it?
Click **Integrations Center** in the sidebar under **Automation & Ecosystem**.

### E. How do I use it?
Each integration card provides four standard buttons:
1. **Test Connection:** Pings the service and displays an immediate success or diagnostic toast.
2. **Connect / Reconnect:**
   - If credentials exist in `.env`, launches the real OAuth consent URL.
   - If unconfigured, connects safely in **Sandboxed Demo Mode** with a single click.
3. **Disconnect (Leads/Admins):** Revokes connection and resets status to `Disconnected`.
4. **Special Action:**
   - **Google Meet:** Click **Discover Drive Artifacts** to scan Google Drive for cloud recordings.
   - **Google Calendar:** Click **Sync Pending Deadlines** to immediately push all approved action items with due dates to Google Calendar.

---

# 6. Governance & Administration Guide

## 6.1 Team Directory & Accountability

### A. What is this page?
The **Team Directory** is an administrative roster of all organization members, their roles, email addresses, departments, and deliverable accountability metrics.

### B. Why do we need it?
Team leads need visibility into workload distribution across their teams without manual status reporting.

### C. Access Control
Restricted to **Administrators** and **Team Leads**. Regular employees attempting access receive a security notice.

### D. How do I open it?
Click **Team Directory** in the sidebar under **Governance**.

### E. How do I use it?
- **Summary Cards:** Total Members, Administrators count, Team Leads count, and Contributors count.
- **Member Roster:** Each card displays:
  - User avatar initial, full name, username, and email.
  - Department and timezone.
  - Role pill (`Admin`, `Team Lead`, `Employee`).
  - Active deliverables count vs Completed count.
  - Color-coded warning if the user has any **Blocked** tasks (e.g., `⚠️ 1 Blocked`).

---

## 6.2 AI Quality Center & Benchmarks

### A. What is this page?
The **AI Quality Center** provides transparent, empirical benchmarking of MeetIntel AI's transcription accuracy, extraction F1 score, and organizational business outcomes.

### B. Why do we need it?
Many AI applications make vague claims about accuracy. MeetIntel AI provides **reproducible benchmarks** tested against human-labeled ground truth to satisfy technical reviewers, internship examiners, and enterprise compliance teams.

### C. When should I use it?
- During an internship review, technical viva, or audit presentation.
- When evaluating whether a new Whisper model or LLM prompt improves extraction accuracy.

### D. How do I open it?
Click **AI Quality & Benchmarks** in the sidebar under **Governance**.

### E. How do I use it?
#### Tab 1: AI Reliability & Benchmark Evaluation
1. Click **✦ Run Reproducible AI Benchmark Evaluation**.
2. In less than a second, MeetIntel AI evaluates reference datasets and displays:
   - **Transcription WER (Word Error Rate):** Measured error rate and accuracy percentage.
   - **Action Item F1 Score:** Precision, Recall, and harmonic F1 score.
   - **Owner Accuracy %:** Percentage of tasks correctly attributed to the speaker who committed to them.
   - **Evidence Grounding %:** Verification that quotes match verbatim transcript turns.
   - **Prompt Injection Defense:** 100% isolation of untrusted user dialogue.
3. Review the **Benchmark Dataset Results Breakdown** table for individual test scenario scores.

#### Tab 2: Organizational Outcome Analytics
- **Meeting-to-Task Conversion Rate:** Percentage of extracted items approved by leadership.
- **Commitment Velocity %:** Percentage of approved tasks successfully completed.
- **Active Blockers Count:** Number of items needing dependency resolution.
- **Verified Decisions Count:** Number of binding agreements active in the organization.

---

## 6.3 Compliance & System Audit Trail

### A. What is this page?
The **Audit Trail** is an immutable, non-repudiable log recording every security, authentication, task, and decision event across the organization.

### B. Why do we need it?
Enterprise compliance standards (SOC2, ISO 27001, HIPAA) require organizations to prove who made decisions, who approved tasks, and who accessed customer data. Entries in this audit trail cannot be edited or deleted.

### C. Access Control
Restricted to **Administrators** and **Team Leads**.

### D. How do I open it?
Click **Audit Trail & Logs** in the sidebar under **Governance**.

### E. How do I use it?
1. **Filter Events:** Filter by **Entity Type** (`task`, `decision`, `meeting`, `calendar`, `notification`, `auth`) or **Action Type** (`APPROVE`, `REJECT`, `UPDATE`, `REASSIGN`, `SYNC`, `LOGIN`).
2. **Review Event Cards:** Each card displays:
   - Action type in brackets: e.g. `[APPROVE]`, `[UPDATE]`, `[LOGIN]`.
   - Entity ID and Type.
   - Plain-English explanation of what changed.
   - Verbatim transcript context (if applicable).
   - Timestamp and Actor username.
3. **Export CSV:** Click **↓ Export Audit Trail (CSV)** to download an immutable compliance log for external auditors.

---

## 6.4 Preferences & System Administration

### A. What is this page?
The **Settings** page configures system environment variables, AI provider credentials, theme styling, and examiner demonstration tools.

### B. Why do we need it?
To change AI models (switching between Gemini, OpenAI, or Demo), update API keys, or switch between light and dark themes without editing raw `.env` files manually.

### C. When should I use it?
- When entering your Gemini or OpenAI API keys for the first time.
- When switching between user personas during a demonstration.
- To seed fresh enterprise demo data before an evaluation presentation.

### D. How do I open it?
Click **Preferences & Settings** in the sidebar under **Governance**.

### E. How do I use it?
1. **Fast Role & Identity Switcher:**
   - Select any user persona from the dropdown (e.g., `Sarah Jenkins (Team Lead)` or `Alex Chen (Employee)`).
   - Click **Switch Identity**. The application immediately updates your session and reruns into that user's view.
2. **Seed Enterprise Demonstration Scenario:**
   - Click **✦ Seed Enterprise Demonstration Scenario**.
   - Populates meeting `demo-meeting-q3-security`, complete transcripts, approved tasks, synced calendar events, and follow-up drafts in seconds.
3. **AI Provider Configuration Form:**
   - **Primary AI Provider:** Choose `Gemini`, `OpenAI`, or `Demo (Local Offline)`.
   - **API Keys:** Enter your `GEMINI_API_KEY` or `OPENAI_API_KEY`.
   - **Whisper Model:** Choose `base`, `small`, `medium`, or `large-v3`.
   - **Hugging Face Token:** Enter your token for speaker diarization.
   - **Theme Preference:** Choose `System ◒`, `Light ☀`, or `Dark ◐`.
   - Click **Save All Settings**. (Persists directly to `.env` and reloads runtime).
4. **System Architecture Status:** Review the runtime status table at the bottom to verify connected libraries.

---

# 7. Specialized Views

## 7.1 Transcript Library

### A. What is this page?
The **Transcript Library** (`ui/transcripts_list.py`) is a dedicated search index focusing purely on verbatim dialogue turns across all recorded meetings.

### B. Why do we need it?
Sometimes you remember an exact phrase someone said (e.g., *"staging replica is provisioned"*), but you do not remember which meeting it was in or who said it. The Transcript Library searches dialogue turns directly.

### C. How do I open it?
Accessible via search routing or direct route `Transcripts`.

### D. How do I use it?
1. Type search keywords into the top search bar.
2. Matching meetings display dialogue snippets.
3. Click **Snippets** to preview the first 3 dialogue turns inline.
4. Click **View** to jump directly into the full Meeting Results Dossier.
