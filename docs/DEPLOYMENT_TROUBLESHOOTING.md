# MeetIntel AI — Deployment Troubleshooting & Runbook

This guide covers common issues encountered during Vercel deployment, database connectivity, OAuth authorization, and background processing, along with exact diagnostic steps and resolutions.

---

## 1. Vercel Build & Runtime Issues

### Issue 1.1: Build Command Fails with "Cannot find module" or "Command not found"
* **Symptom**: Vercel deployment build logs show:
  ```text
  sh: npm run build: command not found OR Error: Cannot find module 'next'
  ```
* **Cause**: Root directory mismatch or missing install command.
* **Resolution**:
  1. Go to **Vercel Project Settings > General**.
  2. If deploying from the repository root:
     - Set **Install Command**: `npm install --prefix web`
     - Set **Build Command**: `npm run build --prefix web`
     - Set **Output Directory**: `web/.next`
  3. Or, change **Root Directory** to `web`:
     - Vercel will automatically run `npm install` and `next build` inside the `web` subfolder.

---

### Issue 1.2: 413 Request Entity Too Large on Audio Uploads
* **Symptom**: Uploading an audio file > 4.5 MB through a Vercel serverless function triggers an HTTP 413 error.
* **Cause**: Vercel serverless functions have a hard 4.5 MB payload limit on request bodies.
* **Resolution**:
  - In production, audio files must be uploaded directly from the browser to S3/R2 object storage using presigned upload URLs (`/api/uploads/presign`), bypassing the Vercel edge proxy.
  - Or route audio uploads to the dedicated containerized backend worker (Render/Railway), which supports files up to 1000 MB.

---

## 2. Database & Persistence Issues

### Issue 2.1: "SSL connection has been closed unexpectedly" or Connection Timeout
* **Symptom**: Serverless function logs report:
  ```text
  sqlalchemy.exc.OperationalError: connection to server at "ep-xyz.us-east-2.aws.neon.tech" failed: SSL connection has been closed unexpectedly
  ```
* **Cause**: Missing SSL parameters or direct connection exhaustion without PgBouncer.
* **Resolution**:
  1. Ensure `sslmode=require` is appended to your `DATABASE_URL`:
     ```text
     postgresql://user:pass@ep-pooler.neon.tech/meetintel?sslmode=require
     ```
  2. For Supabase, use the **Transaction Pooler** connection string (port `6543`), not the direct connection (port `5432`):
     ```text
     postgresql://postgres.xyz:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
     ```

---

### Issue 2.2: "Table does not exist" on fresh database
* **Symptom**: HTTP 500 on first request to `/meetings` or `/tasks`.
* **Cause**: Database tables have not been created in the new managed PostgreSQL instance.
* **Resolution**:
  Run the automated schema initialization script locally once pointing at the production database:
  ```bash
  DATABASE_URL="your-production-postgres-url" python3 -c "from storage.database import init_db; init_db()"
  ```
  This creates all tables (`organizations`, `users`, `meetings`, `action_items`, `decisions`, `audit_events`, etc.) and seeds the default organization and roles.

---

## 3. Integrations & OAuth Issues

### Issue 3.1: Google OAuth Error: `redirect_uri_mismatch` (400)
* **Symptom**: When clicking "Connect Google Workspace", Google displays an error page stating: `Error 400: redirect_uri_mismatch`.
* **Cause**: The redirect URI passed in the OAuth request does not match the URI registered in the Google Cloud Console.
* **Resolution**:
  1. In Google Cloud Console > **Credentials** > select your OAuth 2.0 Client ID.
  2. Under **Authorized redirect URIs**, add the exact public domain of your Vercel deployment:
     ```text
     https://<your-project>.vercel.app/api/google/oauth/callback
     ```
  3. Ensure `GOOGLE_REDIRECT_URI` in Vercel Environment Variables matches this URL exactly (including `https://` protocol and no trailing slash).

---

### Issue 3.2: Zoom Webhook Signature Verification Fails (401 Unauthorized)
* **Symptom**: Zoom webhook requests are rejected with `401 Invalid webhook signature`.
* **Cause**: `ZOOM_WEBHOOK_SECRET` does not match the Secret Token generated in Zoom App Marketplace.
* **Resolution**:
  1. In Zoom App Marketplace > Feature > Event Subscriptions > verify the Secret Token.
  2. Update `ZOOM_WEBHOOK_SECRET` in Vercel Environment Variables and redeploy.

---

## 4. AI Provider & Quota Issues

### Issue 4.1: Google Gemini 429: Resource Exhausted
* **Symptom**: Meeting analysis fails with:
  ```text
  google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded for quota metric 'GenerateContent requests'
  ```
* **Resolution**:
  - The MeetIntel AI `AIProviderManager` (`ai/provider_manager.py`) automatically detects 429 quota exhaustion, marks the primary provider unhealthy for 120 seconds, and immediately fails over to OpenAI `gpt-4o-mini`.
  - Ensure `OPENAI_API_KEY` is configured in Vercel environment variables to allow seamless automated failover.
  - To increase Google Gemini quotas, upgrade your Google AI Studio project to pay-as-you-go billing.

---

## 5. Local Development Issues

### Issue 5.1: Port 8501 or Port 8000 Already in Use
* **Symptom**: `OSError: [Errno 48] Address already in use`
* **Resolution**:
  Find and kill the zombie process:
  ```bash
  # Check port 8501 (Streamlit)
  lsof -i :8501
  kill -9 <PID>

  # Check port 8000 (FastAPI)
  lsof -i :8000
  kill -9 <PID>
  ```

---

### Issue 5.2: Streamlit Session Drops during Local Testing
* **Symptom**: Changing pages in Streamlit resets active filters or selected meeting.
* **Resolution**:
  Ensure you are navigating using the sidebar navigation links rather than browser forward/back buttons. MeetIntel AI manages navigation state via `st.session_state['current_page']`.
