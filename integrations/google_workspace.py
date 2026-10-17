import os
import json
import logging
import datetime
import urllib.parse
from typing import Dict, Any, Optional, List
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Load environment
load_dotenv()

from .crypto import encrypt_token, decrypt_token
from storage import repository, models

logger = logging.getLogger(__name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_CALENDAR_API_BASE = "https://www.googleapis.com/calendar/v3"
GOOGLE_DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email"
]

class GoogleWorkspaceIntegration:
    def __init__(self, org_id: str = "org-default-001"):
        self.org_id = org_id
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/google/oauth/callback")
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true" or not (self.client_id and self.client_secret)

    def is_configured(self) -> bool:
        """Returns True if real client credentials are set in environment."""
        return bool(self.client_id and self.client_secret)

    def get_auth_url(self, state: str = "meetintel_google_state") -> str:
        """Generates Google OAuth 2.0 consent URL with CSRF state."""
        if not self.is_configured():
            return f"mock://google-oauth?state={state}&mode=demo"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        }
        return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

    def exchange_code(self, db: Session, code: str) -> Dict[str, Any]:
        """Exchanges authorization code for access and refresh tokens."""
        if self.demo_mode:
            mock_tokens = {
                "access_token": "demo_google_access_token_xyz",
                "refresh_token": "demo_google_refresh_token_xyz",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            email = "demo.workspace@acmeglobal.io"
            encrypted = encrypt_token(json.dumps(mock_tokens))
            repository.upsert_integration_connection(
                db,
                provider="google_meet",
                connection_status="Connected (Demo)",
                org_id=self.org_id,
                account_email=email,
                encrypted_tokens=encrypted,
                scopes=",".join(SCOPES),
                last_import_result="Successfully simulated Google Workspace connection."
            )
            repository.upsert_integration_connection(
                db,
                provider="google_calendar",
                connection_status="Connected (Demo)",
                org_id=self.org_id,
                account_email=email,
                encrypted_tokens=encrypted,
                scopes=",".join(SCOPES),
                last_import_result="Successfully simulated Google Calendar connection."
            )
            return {"status": "success", "mode": "demo", "email": email}

        try:
            res = requests.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri
                },
                timeout=15
            )
            if res.status_code != 200:
                logger.error(f"Google OAuth token exchange failed: {res.text}")
                return {"status": "error", "message": f"Token exchange failed: {res.text}"}
                
            token_data = res.json()
            # Fetch user email
            userinfo = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                timeout=10
            ).json()
            email = userinfo.get("email", "unknown@google.com")
            
            encrypted = encrypt_token(json.dumps(token_data))
            for provider in ["google_meet", "google_calendar"]:
                repository.upsert_integration_connection(
                    db,
                    provider=provider,
                    connection_status="Connected",
                    org_id=self.org_id,
                    account_email=email,
                    encrypted_tokens=encrypted,
                    scopes=",".join(SCOPES),
                    last_import_result="Live OAuth connection verified."
                )
            return {"status": "success", "mode": "live", "email": email}
        except Exception as e:
            logger.error(f"Google OAuth exchange exception: {e}")
            return {"status": "error", "message": str(e)}

    def get_valid_access_token(self, db: Session, provider: str = "google_calendar") -> Optional[str]:
        """Retrieves and decrypts access token, refreshing if needed."""
        conn = repository.get_integration_connection(db, provider=provider, org_id=self.org_id)
        if not conn or not conn.encrypted_tokens:
            return None
            
        token_json_str = decrypt_token(conn.encrypted_tokens)
        if not token_json_str:
            return None
            
        token_data = json.loads(token_json_str)
        if self.demo_mode or conn.connection_status.endswith("(Demo)"):
            return "demo_google_access_token_xyz"
            
        # Refresh token if present
        if "refresh_token" in token_data:
            try:
                refresh_res = requests.post(
                    GOOGLE_TOKEN_URL,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "refresh_token": token_data["refresh_token"],
                        "grant_type": "refresh_token"
                    },
                    timeout=10
                )
                if refresh_res.status_code == 200:
                    new_tokens = refresh_res.json()
                    token_data["access_token"] = new_tokens["access_token"]
                    conn.encrypted_tokens = encrypt_token(json.dumps(token_data))
                    conn.connection_status = "Connected"
                    db.commit()
                elif refresh_res.status_code in [400, 401]:
                    conn.connection_status = "Needs attention"
                    conn.error_message = "Refresh token expired or revoked. Please reconnect."
                    db.commit()
                    return None
            except Exception as e:
                logger.warning(f"Failed to refresh token: {e}")
                
        return token_data.get("access_token")

    # ---------------------------------------------------------
    # Google Calendar Automation
    # ---------------------------------------------------------

    def sync_task_to_calendar(self, db: Session, task: models.ActionItem, user: models.User, reminders_hours: List[int] = [24, 1]) -> Dict[str, Any]:
        """
        Synchronizes an approved action item to Google Calendar with reminders.
        Prevents duplicate events using idempotency keys.
        """
        idempotency_key = f"gcal_task_{task.id}_{user.id}"
        
        # Check connection status
        conn = repository.get_integration_connection(db, provider="google_calendar", org_id=self.org_id)
        if not conn or "Connected" not in conn.connection_status:
            # Retain approved task locally and mark calendar event as pending
            cal_event = repository.upsert_calendar_event(
                db,
                task_id=task.id,
                meeting_id=task.meeting_id,
                user_id=user.id,
                summary=f"[MeetIntel] {task.task}",
                start_time=datetime.datetime.now(datetime.timezone.utc),
                end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
                org_id=self.org_id,
                sync_status="Pending",
                idempotency_key=idempotency_key
            )
            return {
                "status": "pending_connection",
                "message": "Calendar disconnected. Task saved locally with 'Calendar synchronization pending'.",
                "event_id": cal_event.id
            }

        # Parse deadline date
        start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)
        end_time = start_time + datetime.timedelta(hours=1)
        
        # Check if Demo mode
        if self.demo_mode or conn.connection_status.endswith("(Demo)"):
            mock_ext_id = f"gcal_evt_{task.id}_{idempotency_key[:8]}"
            cal_event = repository.upsert_calendar_event(
                db,
                task_id=task.id,
                meeting_id=task.meeting_id,
                user_id=user.id,
                summary=f"[MeetIntel] {task.task}",
                start_time=start_time,
                end_time=end_time,
                org_id=self.org_id,
                external_event_id=mock_ext_id,
                sync_status="Synced",
                idempotency_key=idempotency_key
            )
            repository.log_audit_event(
                db,
                org_id=self.org_id,
                user_id=user.id,
                actor_username="GoogleCalendarSync",
                entity_type="calendar",
                entity_id=str(cal_event.id),
                action="SYNC",
                details=f"Calendar event synced in Demo mode for task '{task.task}'"
            )
            return {"status": "success", "mode": "demo", "external_event_id": mock_ext_id}

        # Real Google Calendar API call
        access_token = self.get_valid_access_token(db, provider="google_calendar")
        if not access_token:
            return {"status": "error", "message": "Could not obtain valid access token."}

        event_payload = {
            "summary": f"[MeetIntel] {task.task}",
            "description": f"Assigned from meeting: {task.description or task.task}\n\nEvidence Excerpt: {task.evidence_excerpt or 'N/A'}",
            "start": {"dateTime": start_time.isoformat()},
            "end": {"dateTime": end_time.isoformat()},
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "popup", "minutes": h * 60} for h in reminders_hours]
            }
        }

        try:
            res = requests.post(
                f"{GOOGLE_CALENDAR_API_BASE}/calendars/primary/events",
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                json=event_payload,
                timeout=15
            )
            if res.status_code in [200, 201]:
                evt_data = res.json()
                external_id = evt_data["id"]
                cal_event = repository.upsert_calendar_event(
                    db,
                    task_id=task.id,
                    meeting_id=task.meeting_id,
                    user_id=user.id,
                    summary=f"[MeetIntel] {task.task}",
                    start_time=start_time,
                    end_time=end_time,
                    org_id=self.org_id,
                    external_event_id=external_id,
                    sync_status="Synced",
                    idempotency_key=idempotency_key
                )
                return {"status": "success", "mode": "live", "external_event_id": external_id}
            else:
                logger.error(f"Google Calendar API error: {res.text}")
                return {"status": "error", "message": res.text}
        except Exception as e:
            logger.error(f"Google Calendar Sync failed: {e}")
            return {"status": "error", "message": str(e)}

    def sync_all_approved_tasks(self, db: Session) -> int:
        """
        Scans for approved action items within the organization and syncs them to Google Calendar.
        Updates persistent connection synchronization metadata on success.
        """
        approved_tasks = db.query(models.ActionItem).filter(
            models.ActionItem.org_id == self.org_id,
            models.ActionItem.approval_status == "Approved"
        ).all()
        synced_count = 0
        default_user = db.query(models.User).filter(models.User.org_id == self.org_id).first()
        
        for task in approved_tasks:
            existing = db.query(models.CalendarEvent).filter(
                models.CalendarEvent.task_id == task.id,
                models.CalendarEvent.sync_status == "Synced"
            ).first()
            if not existing:
                u = repository.get_user_by_id(db, task.assigned_user_id) if task.assigned_user_id else default_user
                if u:
                    res = self.sync_task_to_calendar(db, task=task, user=u)
                    if res.get("status") == "success":
                        synced_count += 1
                        
        if synced_count > 0:
            conn = repository.get_integration_connection(db, provider="google_calendar", org_id=self.org_id)
            current_status = conn.connection_status if conn else ("Connected (Demo)" if self.demo_mode else "Connected")
            repository.upsert_integration_connection(
                db,
                provider="google_calendar",
                connection_status=current_status,
                org_id=self.org_id,
                account_email=conn.account_email if conn else ("demo.calendar@acmeglobal.io" if self.demo_mode else None),
                last_import_result=f"Synchronized {synced_count} approved task deadline(s) to Google Calendar.",
                last_sync_at=datetime.datetime.now(datetime.timezone.utc)
            )
        return synced_count

    # ---------------------------------------------------------
    # Google Meet Artifacts Discovery
    # ---------------------------------------------------------

    def discover_and_import_artifacts(self, db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Discovers meeting recordings or existing transcripts from Google Drive.
        Avoids redundant transcription if a transcript is already present.
        """
        conn = repository.get_integration_connection(db, provider="google_meet", org_id=self.org_id)
        if not conn or "Connected" not in conn.connection_status:
            return []

        if self.demo_mode or conn.connection_status.endswith("(Demo)"):
            # Return realistic simulated discovery items
            return [
                {
                    "source": "google_meet",
                    "external_id": "gmeet_recording_q3_planning",
                    "title": "Q3 Roadmap & Security Alignment",
                    "date": "2026-10-14",
                    "has_existing_transcript": True,
                    "status": "Ready for 1-Click Import",
                    "file_type": "Google Meet Transcript (.vtt)"
                },
                {
                    "source": "google_meet",
                    "external_id": "gmeet_recording_sprint_retro",
                    "title": "Sprint 42 Architecture Review",
                    "date": "2026-10-15",
                    "has_existing_transcript": False,
                    "status": "Ready for Processing",
                    "file_type": "Cloud Recording (.mp4)"
                }
            ]

        access_token = self.get_valid_access_token(db, provider="google_meet")
        if not access_token:
            return []

        try:
            # Query Drive API for files with 'Meet Recordings' in parents or name
            query = "name contains 'Meet' and (mimeType contains 'video/' or mimeType contains 'text/' or mimeType contains 'document')"
            res = requests.get(
                f"{GOOGLE_DRIVE_API_BASE}/files",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"q": query, "pageSize": 10, "fields": "files(id, name, mimeType, createdTime)"},
                timeout=15
            )
            if res.status_code == 200:
                files = res.json().get("files", [])
                discovered = []
                for f in files:
                    is_transcript = "text" in f["mimeType"] or "document" in f["mimeType"]
                    discovered.append({
                        "source": "google_meet",
                        "external_id": f["id"],
                        "title": f["name"],
                        "date": f.get("createdTime", "")[:10],
                        "has_existing_transcript": is_transcript,
                        "status": "Ready for Import",
                        "file_type": f["mimeType"]
                    })
                return discovered
        except Exception as e:
            logger.error(f"Error querying Google Drive: {e}")
        return []
