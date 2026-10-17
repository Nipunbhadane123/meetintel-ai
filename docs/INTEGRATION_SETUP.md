# MeetIntel AI — Enterprise Integration Setup & Credentials Guide

This guide provides complete, step-by-step instructions for connecting live enterprise integrations in **MeetIntel AI — Meeting-to-Execution Platform**. It covers Google Workspace (Calendar & Meet), Zoom Meetings, and Email (SMTP) notification services.

---

## 1. Multi-Mode Architecture: Live vs. Sandboxed Demo Mode

MeetIntel AI features a multi-mode architecture designed to operate seamlessly in both live production and evaluation environments:

1. **Sandboxed Demo Mode (`DEMO_MODE=true` or missing credentials)**:
   - Connectors simulate API responses, OAuth tokens, and calendar synchronization using verified local reference models.
   - UI status badges display `Connected — Demo` with an indicator flask (`🧪`) to maintain absolute transparency.
   - No external emails, calendar events, or cloud network calls are dispatched.
2. **Verified Live Mode (`DEMO_MODE=false` with valid credentials)**:
   - Real OAuth 2.0 authorization codes are exchanged for cryptographic access & refresh tokens.
   - Tokens are stored encrypted at rest using 32-byte Fernet AES symmetric encryption (`integrations/crypto.py`).
   - Webhook payloads verify HMAC-SHA256 signatures with 300-second timestamp replay protection.
   - Real events and emails are created with idempotency keys to prevent duplicates.

---

## 2. Google Workspace (Google Calendar & Google Meet)

### Prerequisites
- A Google Cloud Platform (GCP) project with billing enabled.
- Administrator access to the Google Workspace domain (for enterprise-wide Meet recordings).

### Step 1: Enable APIs in GCP Console
1. Navigate to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the following APIs:
   - **Google Calendar API**
   - **Google Drive API** (used to discover Meet recordings and transcripts)
   - **Google Meet API**

### Step 2: Configure OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**.
2. Select **Internal** (for your Workspace organization) or **External** (requires test users).
3. Add the following authorized OAuth scopes:
   - `https://www.googleapis.com/auth/calendar.events` (Create and update deadline reminders)
   - `https://www.googleapis.com/auth/drive.readonly` (Read Meet cloud recordings and `.vtt` transcripts)
   - `https://www.googleapis.com/auth/userinfo.email` (Identify connected user email)

### Step 3: Create OAuth 2.0 Client Credentials
1. Go to **Credentials > Create Credentials > OAuth client ID**.
2. Application type: **Web application**.
3. Name: `MeetIntel AI Production`.
4. Authorized Redirect URIs:
   - Local: `http://localhost:8501/api/google/oauth/callback` or `http://localhost:8000/api/google/oauth/callback`
   - Production: `https://your-domain.com/api/google/oauth/callback`
5. Copy the **Client ID** and **Client Secret**.

### Step 4: Configure Environment Variables
```bash
GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="your-client-secret"
GOOGLE_REDIRECT_URI="http://localhost:8501/api/google/oauth/callback"
```

---

## 3. Zoom Meetings Integration

### Prerequisites
- A Zoom account with a Pro, Business, or Enterprise plan (Cloud recording access requires a paid plan).
- Zoom Marketplace developer access.

### Step 1: Create an App in Zoom App Marketplace
1. Navigate to the [Zoom App Marketplace](https://marketplace.zoom.us/).
2. Click **Develop > Build App**.
3. Select **General App** (OAuth) or **Server-to-Server OAuth**.

### Step 2: Configure App Scopes
Add the following required scopes:
- `recording:read` (View and download cloud recordings)
- `meeting:read` (Inspect meeting metadata and participant lists)

### Step 3: Webhook Subscription Configuration
1. In your Zoom App settings, toggle **Event Subscriptions** to ON.
2. Click **Add Event Subscription**:
   - Subscription Name: `MeetIntel Recording Processor`.
   - Event notification endpoint URL: `https://your-domain.com/api/zoom/webhook`.
3. Add Event:
   - Select **Recording > All Recordings have completed** (`recording.completed`).
4. Note your **Secret Token** (used for HMAC signature validation).

### Step 4: Configure Environment Variables
```bash
ZOOM_CLIENT_ID="your-zoom-client-id"
ZOOM_CLIENT_SECRET="your-zoom-client-secret"
ZOOM_WEBHOOK_SECRET="your-zoom-webhook-secret-token"
ZOOM_REDIRECT_URI="http://localhost:8501/api/zoom/oauth/callback"
```

---

## 4. Email Notification Service (SMTP)

### Configuration
MeetIntel AI connects to standard RFC-compliant SMTP servers with TLS encryption (e.g., SendGrid, Amazon SES, Google Workspace SMTP Relay, Microsoft 365).

```bash
SMTP_HOST="smtp.sendgrid.net"
SMTP_PORT=587
SMTP_USER="apikey"
SMTP_PASSWORD="your-smtp-api-key"
SMTP_FROM="notifications@meetintel.ai"
```

### Safety & Delivery Gating
- All attendance-aware follow-up emails require explicit review and approval by a Team Lead or Administrator before dispatch.
- Recipient addresses are strictly validated against existing authorized organization members.
- Duplicate dispatches are prevented using idempotency keys: `followup_{meeting_id}_{user_id}`.

---

## 5. Security & Token Protection Checklist
- [x] Secrets are never logged or returned in user-facing API responses.
- [x] OAuth tokens and secrets are encrypted with Fernet AES-256 before writing to the database.
- [x] Zoom webhooks reject requests with missing or expired timestamps (> 300 seconds).
- [x] Cross-tenant isolation is enforced on every operation using `org_id`.
