# MeetIntel AI — Feature Verification & Quality Assurance Checklist

**Document Version:** 2.0.0  
**Automated Test Baseline:** 64 of 64 Tests Passing (`pytest tests/`)  
**Manual Test Execution Status:** Template ready for operator verification.

---

## 1. Automated Test Suite Execution Baseline

The automated test suite verifies all underlying Python functions, API routes, database schemas, role checks, and encryption logic.

### Automated Test Summary
```
============================= test session starts ==============================
Platform: macOS (Darwin 24.3.0), Python 3.12.8, Pytest 9.1.1
Collected: 64 items

tests/test_api.py .................................................... [  6%]
tests/test_auth.py ................................................... [  7%]
tests/test_auth_flow.py .............................................. [ 23%]
tests/test_e2e.py .................................................... [ 25%]
tests/test_enterprise_workflows.py ................................... [ 56%]
tests/test_master_journeys.py ........................................ [ 65%]
tests/test_milestone2.py ............................................. [ 75%]
tests/test_projects.py ............................................... [ 87%]
tests/test_ui_components.py .......................................... [100%]

============================= 64 passed in 26.25s ==============================
```

---

## 2. Manual Verification Checklist

Use this checklist to manually test and sign off on features in the running Streamlit web application.

### Legend
- `[ ]` Test Not Yet Executed
- `[x]` Test Executed & Passed
- `[FAIL]` Test Failed

---

### Section 1: Authentication, Access Control & Tenant Isolation

#### TC-AUTH-01: Valid User Login
- **Preconditions:** Application running at `http://localhost:8501`. User `admin` exists.
- **Test Data:** Username: `admin`, Password: `admin123`.
- **Steps:**
  1. Open `http://localhost:8501`.
  2. Enter credentials on Login tab.
  3. Click **Sign in**.
- **Expected Outcome:** Login succeeds; user lands on Overview Dashboard with header *"Good [morning/afternoon/evening], Admin"*. An audit event of type `LOGIN` is recorded.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`
- **Recovery Instructions:** If password fails, run `PYTHONPATH=. .venv/bin/python scripts/admin_recovery.py --username admin --password "admin123"`.

#### TC-AUTH-02: Invalid Password Rejection
- **Preconditions:** Application running.
- **Test Data:** Username: `admin`, Password: `wrongpassword999`.
- **Steps:**
  1. On login screen, enter username and incorrect password.
  2. Click **Sign in**.
- **Expected Outcome:** Login blocked. Red error message displayed: *"Invalid username or password."* User remains on login screen. Audit event `LOGIN_FAILED` recorded.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-AUTH-03: Employee Role Gate (Access Restriction)
- **Preconditions:** Logged in as `alex_eng` (Role: `Employee`).
- **Test Data:** Navigation to Team Directory.
- **Steps:**
  1. Attempt to open Team Directory. (In sidebar, notice it is hidden from Employees; if manually navigated to `Team & Organization`):
- **Expected Outcome:** UI renders red security banner: *"🛡️ Access Restricted: You must be a Team Lead or Organization Administrator to access the Team Directory."*
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-AUTH-04: Fast Identity Switcher (Demo Tool)
- **Preconditions:** Logged in.
- **Test Data:** Switching identity to `Sarah Jenkins (Team Lead)`.
- **Steps:**
  1. Open **Preferences & Settings**.
  2. In **Fast Role & Identity Switcher**, select `Sarah Jenkins (Team Lead)`.
  3. Click **Switch Identity**.
- **Expected Outcome:** Page reruns. Sidebar now shows Governance section items (Team Directory, AI Quality, Audit Trail). Profile displays Sarah Jenkins.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

---

### Section 2: Ingestion, Validation & Meeting Processing

#### TC-ING-01: Audio File Validation & Metadata Inspection
- **Preconditions:** On **Process Meeting** page.
- **Test Data:** `test_meeting.wav`.
- **Steps:**
  1. Upload `test_meeting.wav` in the file uploader.
- **Expected Outcome:** Validation passes. File specs container appears showing size, duration, format (`WAV`), and status pill `Validated & Ready`.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-ING-02: Deduplication Detection
- **Preconditions:** An audio file that was already processed exists in the library.
- **Test Data:** Same audio file uploaded again.
- **Steps:**
  1. Upload the exact same audio file.
- **Expected Outcome:** Status badge displays `Already Processed`. Information box warns: *"This exact meeting audio has already been processed and analyzed. You can view the results directly."* Button **▶ View Meeting Results** is rendered.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-ING-03: Full AI Processing Pipeline
- **Preconditions:** Audio file validated and ready.
- **Steps:**
  1. Click **▶ Start AI Processing**.
  2. Observe progress bar through all 5 stages (Audio extraction -> Transcription -> Speaker identification -> AI analysis -> Knowledge indexing).
- **Expected Outcome:** Progress reaches 100%. Status box turns green *"Processing complete!"*. Application automatically redirects to the 8-tab **Meeting Results Dossier**.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

---

### Section 3: Meeting Dossier & Intelligence Verification

#### TC-DOS-01: Executive Overview Verification
- **Preconditions:** Meeting dossier opened.
- **Steps:**
  1. Click the **Overview** tab.
- **Expected Outcome:** Renders narrative Executive Summary, Meeting Objective, Emotional Tone, Key Topics, Discussion Points, Recommendations, and Risks table with impact levels.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-DOS-02: Verbatim Evidence Quote Inspection
- **Preconditions:** Meeting dossier opened.
- **Steps:**
  1. Click the **Action Items** tab.
  2. Inspect the **Source Evidence Box** on the first task card.
- **Expected Outcome:** Displays the exact quoted sentence from the meeting transcript inside an evidence quote container.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-DOS-03: Multi-Format MoM Report Exports
- **Preconditions:** Meeting dossier opened.
- **Steps:**
  1. Click the **MoM** tab.
  2. Click **📄 Download PDF**.
  3. Click **📝 Download Word**.
  4. Click **📊 Download CSV**.
  5. Click **📃 Download TXT**.
- **Expected Outcome:** Each button triggers a valid file download. Opening the PDF shows styled headings, tables, and DejaVu typography without formatting corruption.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-DOS-04: Word Error Rate (WER) Speech Accuracy Benchmark
- **Preconditions:** Meeting dossier opened -> **Transcript** tab.
- **Steps:**
  1. Expand **📊 Speech Recognition Accuracy Assessment**.
  2. Paste a reference sentence into the text area.
  3. Click **Evaluate Accuracy & WER**.
- **Expected Outcome:** Calculates and displays mathematical **Word Recognition Accuracy %** and **Word Error Rate (WER)**.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

---

### Section 4: Task Execution & Commitment Management

#### TC-TASK-01: Task Status Transition & Notes Logging
- **Preconditions:** On **My Commitments** page.
- **Test Data:** Status: `In Progress`, Notes: `Unit tests written and verified.`
- **Steps:**
  1. On any active task card, change status dropdown to `In Progress`.
  2. Enter notes into text box.
  3. Click **Update**.
- **Expected Outcome:** Toast confirms update. Task card displays progress notes callout box.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-TASK-02: Blocker Escalation
- **Preconditions:** On **My Commitments** page.
- **Steps:**
  1. Select `Blocked` from the status dropdown.
  2. Enter blocker explanation: `Waiting for API key`.
  3. Click **Update**.
- **Expected Outcome:** Task immediately transitions to the **Blocked & Overdue** tab. Overview dashboard reflects an increment in the **Blockers & Risks** KPI card.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-TASK-03: Team Lead Task Approval & Calendar Sync
- **Preconditions:** Logged in as `Team Lead`.
- **Steps:**
  1. Under **Management Actions**, click **✓ Approve Task**.
- **Expected Outcome:** Approval badge updates to green `Approved`. Calendar sync pill reflects `Synced` (or `Synced (Demo)`). Audit log records `APPROVE` action.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

---

### Section 5: Projects, Decisions & Knowledge Search

#### TC-PROJ-01: Project Creation & Progress Computation
- **Preconditions:** On **Projects & Milestones** page (Lead/Admin).
- **Test Data:** Name: `QA Automation Framework`, Status: `Active`.
- **Steps:**
  1. Fill in **Register Strategic Project** form.
  2. Click **Save Strategic Initiative**.
- **Expected Outcome:** New project appears in list with completion percentage progress bar and target milestone date.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-DEC-01: Decision Revision & Superseding
- **Preconditions:** On **Decision Register** page (Lead/Admin).
- **Steps:**
  1. On an approved decision, expand **⚙️ Supersede / Revise Decision**.
  2. Enter replacement decision text.
  3. Click **Confirm Revision & Mark Superseded**.
- **Expected Outcome:** Original decision status becomes `Superseded`. New decision is created as `Approved`. Audit log records superseding event.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-RAG-01: Grounded Knowledge Search (Ask AI)
- **Preconditions:** On **Organizational Knowledge** page.
- **Test Data:** Question: `What decisions were made regarding security?`
- **Steps:**
  1. Select **✨ Grounded Ask AI**.
  2. Type question into chat input and press Enter.
- **Expected Outcome:** AI responds with a synthesized, factual answer. Source chips appear below referencing the meeting title and dialogue turns.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

---

### Section 6: Governance, Automations & Integrations

#### TC-AUTO-01: Manual Background Worker Trigger
- **Preconditions:** On **Workflow Automations** page -> **Job Queue Log** tab.
- **Steps:**
  1. Click **⚡ Run Worker Batch Now**.
- **Expected Outcome:** Toast notification displays: *"Worker processed N background job(s)!"*. Queued jobs transition to `COMPLETED`.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-INT-01: Integration Connection Health Ping
- **Preconditions:** On **Integrations Center** page.
- **Steps:**
  1. Click **Test Connection** on the Google Workspace or Zoom card.
- **Expected Outcome:** Service responds with a verified health message (e.g. *"Google Workspace connection operational"*).
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-QUAL-01: Reproducible AI Benchmark Runner
- **Preconditions:** On **AI Quality & Benchmarks** page.
- **Steps:**
  1. Click **✦ Run Reproducible AI Benchmark Evaluation**.
- **Expected Outcome:** Benchmark runner executes against labeled datasets. Metric cards render measured WER, F1 score, Owner Accuracy, and Grounding %. Results table displays individual test case breakdowns.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`

#### TC-AUD-01: Immutable Audit Trail Export
- **Preconditions:** On **Audit Trail & Logs** page.
- **Steps:**
  1. Filter by entity type or action.
  2. Click **↓ Export Audit Trail (CSV)**.
- **Expected Outcome:** Browser downloads `Compliance_Audit_Trail.csv` containing timestamps, actors, actions, and details.
- **Actual Outcome:** `________________________________________`
- **Status:** `[ ] PASS` / `[ ] FAIL`
