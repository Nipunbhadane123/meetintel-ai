# MeetIntel AI — Production Vercel Deployment Guide

**Product Positioning**: AI-Powered Meeting Intelligence & Meeting-to-Execution SaaS  
**Target Platform**: Vercel (Frontend & Serverless Orchestration) + Managed PostgreSQL + S3 Storage + Dedicated ML Worker  
**Repository**: `https://github.com/HARICHARAN8/meetintel-ai.git`

---

## 1. Architecture Overview

MeetIntel AI uses an enterprise **Hybrid Production Architecture** (Option D):

```mermaid
flowchart TD
    subgraph Vercel Cloud
        V1[Next.js 16 Web Application]
        V2[Serverless Request Routes / Edge]
    end

    subgraph Managed Cloud Infrastructure
        DB[(Managed PostgreSQL - Neon / Supabase)]
        S3[(Persistent S3 Object Storage - AWS / R2)]
        AI[Google Gemini & OpenAI APIs]
    end

    subgraph Dedicated Worker Cluster
        W1[Audio Processing Worker - Docker / Render]
        W2[Faster-Whisper & Pyannote Engine]
    end

    Users[Enterprise Users & Team Leads] -->|HTTPS| V1
    V1 -->|Direct Presigned Upload| S3
    V1 -->|API Requests| V2
    V2 -->|Connection Pooler 6543| DB
    V2 -->|REST API| AI
    W1 -->|Polls background_jobs| DB
    W1 -->|Downloads Audio| S3
    W1 -->|Transcribes & Diarizes| W2
```

- **Frontend on Vercel**: High-performance Next.js web application delivering the full 15-view suite, real-time filters, interactive task approval, decision register, RAG semantic search, and Minutes of Meeting (MoM) export.
- **Database on Managed PostgreSQL**: Neon or Supabase PostgreSQL with connection pooling (`DATABASE_URL`).
- **Object Storage**: AWS S3, Cloudflare R2, or Supabase Storage for persistent recordings and MoM documents.
- **Dedicated Worker (Optional for live audio)**: Containerized worker for heavy Whisper (`faster-whisper`) and Pyannote (`pyannote.audio`) models.
- **Local Development**: Streamlit (`app.py`, `ui/`) and FastAPI (`api/main.py`) remain 100% functional locally for rapid pair programming and debugging.

---

## 2. Step-by-Step Deployment Instructions

### Step 1: Prepare the Repository & Run Local Verification
Ensure your local branch is clean and all automated tests pass:

```bash
# 1. Activate your virtual environment
source .venv/bin/activate

# 2. Run the test suite
PYTHONPATH=. pytest tests/ -k "not test_full_pipeline_with_real_llm"

# 3. Verify Next.js web build
npm run build --prefix web
```

Expected result:
- 69 tests pass.
- Next.js compiles all 18 routes in ~2 seconds.

---

### Step 2: Configure External Services

#### A. Managed PostgreSQL Database (Neon or Supabase)
1. Sign in to [Neon Console](https://console.neon.tech) or [Supabase](https://supabase.com).
2. Create a new project: `meetintel-production`.
3. In Connection Details, copy the **Pooled Connection String** (PgBouncer):
   ```text
   postgresql://username:password@ep-sample-pooler.us-east-2.aws.neon.tech/meetintel?sslmode=require
   ```

#### B. Google Cloud Console (Google Meet & Google Calendar)
1. Navigate to [Google Cloud Console](https://console.cloud.google.com).
2. Create or select your project: `MeetIntel AI Production`.
3. Go to **APIs & Services** > **OAuth consent screen** (Internal or External).
4. Add scopes:
   - `https://www.googleapis.com/auth/calendar.events`
   - `https://www.googleapis.com/auth/drive.readonly`
5. Go to **Credentials** > **Create Credentials** > **OAuth Client ID** (Web application).
6. Set **Authorized redirect URIs**:
   - `https://<your-vercel-domain>.vercel.app/api/google/oauth/callback`
   - `http://localhost:8000/api/google/oauth/callback` (for local testing)
7. Save your `Client ID` and `Client Secret`.

#### C. Zoom App Marketplace (Optional Cloud Webhooks)
1. Navigate to [Zoom App Marketplace](https://marketplace.zoom.us).
2. Create a **Server-to-Server OAuth** or **Webhook Only** app.
3. Event Subscriptions: Add `recording.completed`.
4. Event Notification Endpoint URL:
   - `https://<your-vercel-domain>.vercel.app/api/zoom/webhook`
5. Copy your **Verification Secret Token**.

#### D. AI Providers
1. **Google Gemini**: Get an API key from [Google AI Studio](https://aistudio.google.com/).
2. **OpenAI**: Get an API key from [OpenAI Platform](https://platform.openai.com/).

---

### Step 3: Create & Configure Project in Vercel

#### Method 1: Via Vercel Web Dashboard (Recommended)
1. Log in to your [Vercel Dashboard](https://vercel.com).
2. Click **Add New...** > **Project**.
3. Under **Import Git Repository**, select your GitHub repository: `HARICHARAN8/meetintel-ai`.
4. In the **Configure Project** step:
   - **Project Name**: `meetintel-ai`
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `web` (or leave as `.` since root `vercel.json` automatically handles `--prefix web`).
   - **Build Command**: `npm run build` (or `npm run build --prefix web`)
   - **Output Directory**: `.next` (or `web/.next`)
5. Click **Environment Variables** (expand section) and add the variables listed in Section 3 below.
6. Click **Deploy**.

#### Method 2: Via Vercel CLI
```bash
# Install Vercel CLI globally (if desired)
npm install -g vercel

# Link and deploy from root
vercel link
vercel env pull .env.production.local
vercel --prod
```

---

## 3. Environment Variable Reference

Configure these variables in **Vercel Project Settings > Environment Variables**:

| Variable Name | Required | Environment | Purpose | Example Value |
| :--- | :---: | :--- | :--- | :--- |
| `ENV` | Yes | Production, Preview | Execution mode | `production` |
| `SECRET_KEY` | Yes | Production, Preview | Symmetric encryption for OAuth tokens & session cookies | `generate-random-32-char-string` |
| `DATABASE_URL` | Yes | Production, Preview | Managed PostgreSQL connection string | `postgresql://user:pass@pooler.neon.tech/meetintel?sslmode=require` |
| `API_KEY` | Yes | Production, Preview | Internal service security key | `your-secure-internal-api-key` |
| `GEMINI_API_KEY` | Yes | Production, Preview | Primary AI intelligence provider | `AIzaSy...` |
| `GEMINI_PRIMARY_MODEL` | No | Production, Preview | Default Google model | `gemini-2.5-flash` |
| `OPENAI_API_KEY` | Optional | Production, Preview | Fallback AI provider | `sk-proj-...` |
| `AI_PRIMARY_PROVIDER` | Yes | Production, Preview | Primary provider flag | `gemini` |
| `DEMO_MODE` | No | Production | Restricts mock data in production | `false` |
| `ADMIN_EMAIL` | Yes | Production | System administrator email | `admin@yourdomain.com` |
| `ADMIN_PASSWORD` | Yes | Production | Initial bootstrap admin password | `YourStrongSecurePassword123!` |
| `GOOGLE_CLIENT_ID` | Optional | Production | Google Workspace OAuth client | `123456...apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET`| Optional | Production | Google Workspace OAuth secret | `GOCSPX-...` |
| `GOOGLE_REDIRECT_URI` | Optional | Production | Public callback endpoint | `https://meetintel-ai.vercel.app/api/google/oauth/callback` |
| `SMTP_HOST` | Optional | Production | Mail server host | `smtp.resend.com` or `smtp.sendgrid.net` |
| `SMTP_PORT` | Optional | Production | Mail server port | `587` |
| `SMTP_USER` | Optional | Production | SMTP username | `resend` |
| `SMTP_PASSWORD` | Optional | Production | SMTP API password | `re_...` |
| `SMTP_FROM` | Optional | Production | From email address | `notifications@yourdomain.com` |

---

## 4. Verification & Testing

### 1. Test Preview Deployment
Before promoting to production, Vercel creates a Preview URL on pull requests or git pushes.
Verify the preview:
1. Open the preview URL: `https://meetintel-ai-git-<branch>.vercel.app`.
2. Verify all 15 views render cleanly with zero 404 or hydration errors.
3. Switch user roles using the top-bar dropdown (Admin -> Team Lead -> Employee) and verify role badges adapt.
4. Open the **Meeting Intelligence Dossier** (`/meetings/demo-meeting-q3-security`) and verify all 8 tabs (Overview, Action Items, Participants, Deadlines, Priorities, Transcript, Ask AI, MoM).
5. Click **Download PDF** and **Download Word** to verify export triggers.
6. Open **Integrations Center** (`/integrations`) and click **Test Connection** on Google Calendar and SMTP. Verify latency metrics report 200 OK.
7. Open **Workflow Automations** (`/automations`) and click **Test Run Trigger** to verify rule execution.

### 2. Promote to Production
```bash
# Push to main branch
git push origin main
```
Vercel will automatically build and publish to your primary production domain: `https://meetintel-ai.vercel.app`.

---

## 5. Custom Domain Configuration (Optional)

1. In Vercel Project Settings, navigate to **Domains**.
2. Click **Add** and enter your custom domain (e.g., `meetintel.yourdomain.com` or `app.meetintel.ai`).
3. Add the DNS records provided by Vercel to your DNS registrar (Cloudflare, GoDaddy, Route 53):
   - **Type**: `CNAME`
   - **Name**: `app` (or subdomain)
   - **Value**: `cname.vercel-dns.com`
4. Once verified, update your Google OAuth redirect URI in Google Cloud Console:
   - `https://app.meetintel.ai/api/google/oauth/callback`

---

## 6. Rollback & Disaster Recovery

If an issue occurs in production:
1. Go to **Deployments** in your Vercel Dashboard.
2. Locate the last stable deployment.
3. Click the three dots (`...`) next to the deployment and select **Instant Rollback**.
4. Traffic is immediately shifted back to the previous deployment in under 500ms without rebuilding.

---

## 7. Ongoing Maintenance & Git Workflow

- **Branch Deploys**: Every commit to a feature branch (`feat/*`, `fix/*`) automatically builds an isolated Vercel Preview URL with comment bots.
- **Production Releases**: Merging to `main` deploys to production.
- **Local Developer Workflow**: Developers can continue running:
  ```bash
  # Option A: Next.js Frontend
  npm run dev --prefix web

  # Option B: Streamlit Python UI
  streamlit run app.py
  ```
