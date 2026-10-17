# MeetIntel AI — Integration Troubleshooting & Diagnostic Runbook

This guide covers verified solutions to the most common setup errors encountered when integrating MeetIntel AI with Google Workspace, Zoom, SMTP email, and AI providers.

---

## 1. Google OAuth Issues

### Issue 1.1: `Access blocked: MeetIntel AI has not completed the Google verification process` (Error 403: access_denied)
- **Root Cause:** When a Google Cloud project is in **Testing** publishing status, Google blocks every user account by default unless they are explicitly added to the **Test users** list in the OAuth Consent Screen.
- **Fix Procedure:**
  1. Go to [Google Cloud Console](https://console.cloud.google.com/).
  2. Select your project $\rightarrow$ Go to **APIs & Services > OAuth consent screen**.
  3. Scroll down to the **Test users** section.
  4. Click **+ Add Users**.
  5. Enter the exact Google email address you are attempting to log in with.
  6. Click **Save** and retry the authorization link in MeetIntel AI.

---

### Issue 1.2: `Error 400: redirect_uri_mismatch`
- **Root Cause:** The redirect URI sent by the application does not match the exact string entered in the Google Cloud Console Credentials tab (including trailing slashes or port numbers).
- **Fix Procedure:**
  1. Open `.env` and check your `GOOGLE_REDIRECT_URI`. It should be:
     ```env
     GOOGLE_REDIRECT_URI=http://localhost:8000/api/google/oauth/callback
     ```
  2. In Google Cloud Console, go to **APIs & Services > Credentials**.
  3. Click your **OAuth 2.0 Client ID** to edit it.
  4. Under **Authorized redirect URIs**, ensure BOTH of the following are listed:
     - `http://localhost:8000/api/google/oauth/callback`
     - `http://localhost:8501/api/google/oauth/callback`
  5. Click **Save** (changes take effect within 1 minute).

---

### Issue 1.3: Google Meet Shows "Account: Not linked" and "Connection failed"
- **Root Cause:** The database does not yet contain a valid OAuth access/refresh token for `google_meet`. This happens before the user completes the OAuth authorization workflow or if an earlier session expired.
- **Fix Procedure:**
  1. Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in `.env`.
  2. In MeetIntel AI, click **✦ Authorize Google Workspace**.
  3. Complete the Google consent screen in your browser.
  4. Once redirected, refresh the Integrations page.

---

## 2. Google Calendar Issues

### Issue 2.1: Disconnected Status Contradicted by Stale Synchronization Message
- **Root Cause:** In earlier versions of `integrations/google_workspace.py`, when the calendar was disconnected, pending local saves (`pending_connection`) were mistakenly counted as successful syncs, leaving behind a misleading message.
- **Resolution:**
  - Repaired in code: `sync_all_approved_tasks` only counts confirmed HTTP 200/201 responses from the Google Calendar API.
  - Stale database records were cleaned up. When disconnected, the card now accurately displays:
    `Status: Disconnected` | `Last Recorded Sync: (Prior Session)` | `Result: Disconnected: Disconnected by administrator.`

---

## 3. Zoom Integration Issues

### Issue 3.1: Zoom Card Displays "Connected — Demo"
- **Root Cause:** Without `ZOOM_CLIENT_ID` and `ZOOM_CLIENT_SECRET` in `.env`, MeetIntel AI operates in **Sandboxed Demo Mode**. Clicking "Connect" enables the local simulation environment so you can test meeting intelligence without a paid Zoom subscription.
- **Resolution:**
  - If you have a paid Zoom account, add your credentials to `.env`:
    ```env
    ZOOM_CLIENT_ID=your-client-id
    ZOOM_CLIENT_SECRET=your-client-secret
    ZOOM_WEBHOOK_SECRET=your-webhook-secret
    ```
  - If you do not have a paid Zoom account, use the **Sandboxed Demo Mode** or upload test audio files directly via the **New Meeting** tab.

---

### Issue 3.2: Webhook Endpoint URL Validation Fails in Zoom Marketplace
- **Root Cause:** When setting up webhooks, Zoom sends a test challenge payload (`endpoint.url_validation`) with a `plainToken`. Zoom requires an HMAC-SHA256 encrypted response.
- **Resolution:**
  - MeetIntel AI automatically handles this challenge in `integrations/zoom_service.py` via `handle_endpoint_url_validation`.
  - For local development, expose your FastAPI port 8000 using ngrok:
    ```bash
    ngrok http 8000
    ```
  - Use `https://your-ngrok-domain.ngrok-free.app/api/zoom/webhook` as your event notification endpoint in Zoom.

---

## 4. Authentication & Login Issues

### Issue 4.1: `Invalid username or password` on Login Page
- **Root Cause:**
  1. Trying default password `admin` when the actual database seed is `admin123`.
  2. Setting `ADMIN_PASSWORD` in `.env` to a placeholder or expecting `.env` to overwrite the existing database record automatically.
- **Fix Procedure:**
  1. Try logging in with:
     - **Username:** `admin`
     - **Password:** `admin123`
  2. Or run the non-destructive recovery CLI in macOS Terminal:
     ```bash
     .venv/bin/python scripts/admin_recovery.py
     ```
     Enter your preferred password interactively. All existing meetings and database records will be strictly preserved.

---

## 5. AI Provider Issues

### Issue 5.1: `404 NOT_FOUND: models/gemini-1.5-pro is not found`
- **Root Cause:** The `gemini-1.5-pro` identifier is not supported for generateContent in the latest `v1beta` endpoint in this environment.
- **Resolution:**
  - In `.env`, ensure your fallback list uses modern flash models:
    ```env
    GEMINI_PRIMARY_MODEL=gemini-3.6-flash
    GEMINI_FALLBACK_MODELS=gemini-3.5-flash-lite,gemini-2.5-flash
    ```
  - Run `.venv/bin/python scripts/check_gemini.py` to verify all models report `PASS`.

---

## 6. Speaker Diarization Issues

### Issue 6.1: `HUGGINGFACE_TOKEN environment variable not set` or `403 Forbidden`
- **Root Cause:** Pyannote requires explicit license agreement on Hugging Face before tokens can download model weights.
- **Fix Procedure:**
  1. Visit [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1).
  2. Ensure you are signed in and click **Agree and access repository**.
  3. Generate a Hugging Face user access token under **Settings > Access Tokens**.
  4. Paste into `.env`:
     ```env
     HUGGINGFACE_TOKEN=hf_...
     ```
