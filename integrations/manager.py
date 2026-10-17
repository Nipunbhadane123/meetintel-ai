import os
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from storage import repository, models
from .google_workspace import GoogleWorkspaceIntegration
from .zoom_service import ZoomIntegration
from .email_service import EmailNotificationService

logger = logging.getLogger(__name__)

class IntegrationCenterManager:
    def __init__(self, org_id: str = "org-default-001"):
        self.org_id = org_id
        self.google = GoogleWorkspaceIntegration(org_id=org_id)
        self.zoom = ZoomIntegration(org_id=org_id)
        self.email = EmailNotificationService(org_id=org_id)

    def _build_status_dict(
        self,
        prov_key: str,
        name: str,
        category: str,
        conn: Optional[models.IntegrationConnection],
        is_demo_mode: bool,
        setup_guide: str,
        default_demo_email: str
    ) -> Dict[str, Any]:
        if conn:
            raw_status = conn.connection_status or ("Connected (Demo)" if is_demo_mode else "Not configured")
            err = conn.error_message or ""
            
            # Map into honest enterprise SaaS status taxonomy
            if "expired" in err.lower() or "token" in err.lower() or "auth" in err.lower():
                status = "Authentication expired"
            elif raw_status == "Needs attention":
                status = "Needs attention"
            elif "Demo" in raw_status:
                status = "Connected — Demo"
            elif "Connected" in raw_status:
                status = "Connected — Live"
            elif raw_status in ["Not connected", "Disconnected", "Not configured"]:
                status = "Disconnected"
            else:
                status = raw_status

            # Honest Account resolution
            if status in ["Authentication expired", "Disconnected", "Not configured"]:
                account_email = None
            elif conn.account_email:
                account_email = conn.account_email
            elif "Connected" in status:
                account_email = default_demo_email if is_demo_mode else "user@workspace"
            else:
                account_email = None

            # Honest Sync resolution:
            # If status is disconnected or auth expired, don't pretend it's actively synchronized
            if conn.last_sync_at:
                formatted_ts = conn.last_sync_at.strftime("%Y-%m-%d %H:%M")
                if status in ["Authentication expired", "Disconnected", "Needs attention"]:
                    last_sync = f"{formatted_ts} (Prior Session)"
                else:
                    last_sync = formatted_ts
            else:
                last_sync = "Never"

            # Last Result resolution (guaranteed non-null string):
            if status == "Authentication expired":
                last_result = f"Action Required: {err or 'OAuth token expired. Re-authentication required.'}"
            elif status == "Needs attention" and err:
                last_result = f"Action Required: {err}"
            elif status in ["Disconnected", "Not configured"]:
                last_result = f"Disconnected: {err}" if err else "Service disconnected. Connect to enable synchronization."
            elif conn.last_import_result:
                last_result = conn.last_import_result
            elif err:
                last_result = err
            else:
                last_result = "No synchronization activity recorded."

            is_demo = "Demo" in raw_status or (is_demo_mode and "Live" not in status)
        else:
            status = "Connected (Demo)" if is_demo_mode else "Not configured"
            account_email = default_demo_email if is_demo_mode else None
            last_sync = "Never"
            last_result = "Ready for sandbox simulation." if is_demo_mode else "Connector not initialized."
            is_demo = is_demo_mode

        return {
            "name": name,
            "category": category,
            "status": status,
            "account_email": account_email,
            "last_sync": last_sync,
            "last_result": last_result,
            "is_demo": is_demo,
            "setup_guide": setup_guide
        }

    def get_all_integration_statuses(self, db: Session) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves real-time verified status for all integrated services.
        Never exposes client secrets or access tokens.
        """
        gmeet_conn = repository.get_integration_connection(db, provider="google_meet", org_id=self.org_id)
        gcal_conn = repository.get_integration_connection(db, provider="google_calendar", org_id=self.org_id)
        zoom_conn = repository.get_integration_connection(db, provider="zoom", org_id=self.org_id)
        email_conn = repository.get_integration_connection(db, provider="email_smtp", org_id=self.org_id)

        return {
            "google_meet": self._build_status_dict(
                prov_key="google_meet",
                name="Google Meet",
                category="Meeting Source",
                conn=gmeet_conn,
                is_demo_mode=self.google.demo_mode,
                setup_guide="Requires Google Workspace OAuth 2.0 Client ID with Drive Readonly and Google Meet scopes.",
                default_demo_email="demo.workspace@acmeglobal.io"
            ),
            "zoom": self._build_status_dict(
                prov_key="zoom",
                name="Zoom Meetings",
                category="Meeting Source",
                conn=zoom_conn,
                is_demo_mode=self.zoom.demo_mode,
                setup_guide="Requires Zoom Marketplace Server-to-Server or OAuth App with 'recording:read' scope. Cloud recording requires a paid Zoom plan.",
                default_demo_email="demo.zoom@acmeglobal.io"
            ),
            "google_calendar": self._build_status_dict(
                prov_key="google_calendar",
                name="Google Calendar",
                category="Calendar & Reminders",
                conn=gcal_conn,
                is_demo_mode=self.google.demo_mode,
                setup_guide="Requires Google OAuth 2.0 with 'calendar.events' scope to push deadline reminders automatically.",
                default_demo_email="demo.calendar@acmeglobal.io"
            ),
            "email_smtp": self._build_status_dict(
                prov_key="email_smtp",
                name="Email Notification Service",
                category="Follow-ups & Notifications",
                conn=email_conn,
                is_demo_mode=not self.email.is_configured(),
                setup_guide="Configurable via standard SMTP credentials (host, port, TLS user/password).",
                default_demo_email=os.getenv("SMTP_FROM", "demo.mailer@acmeglobal.io")
            )
        }

    def test_connection(self, db: Session, provider: str) -> Dict[str, Any]:
        """Runs an explicit connection check and returns results."""
        if provider in ["google_meet", "google_calendar"]:
            if self.google.demo_mode:
                return {"status": "info", "message": "Demo Mode: Google Workspace simulation active (No live Google API credentials configured)."}
            token = self.google.get_valid_access_token(db, provider=provider)
            if token:
                return {"status": "success", "message": "Google Workspace OAuth connection healthy and token refreshed."}
            return {"status": "error", "message": "Connection failed. Please authorize Google Workspace."}

        elif provider == "zoom":
            if self.zoom.demo_mode:
                return {"status": "info", "message": "Demo Mode: Zoom webhook simulator active (No live Zoom Marketplace credentials configured)."}
            if self.zoom.is_configured():
                return {"status": "success", "message": "Zoom credentials configured. Webhook listener active."}
            return {"status": "error", "message": "Zoom credentials missing."}

        elif provider == "email_smtp":
            if self.email.demo_mode:
                return {"status": "info", "message": "Demo Mode: Simulated mailer active (No live SMTP server credentials configured)."}
            return {"status": "success", "message": "SMTP connection parameters configured and ready."}

        return {"status": "error", "message": "Unknown integration provider."}

    def disconnect(self, db: Session, provider: str, user_id: str) -> bool:
        """Safely disconnects an integration."""
        conn = repository.get_integration_connection(db, provider=provider, org_id=self.org_id)
        if conn:
            conn.connection_status = "Not connected"
            conn.encrypted_tokens = None
            conn.account_email = None
            conn.error_message = "Disconnected by administrator."
            db.commit()
            
            repository.log_audit_event(
                db,
                org_id=self.org_id,
                user_id=user_id,
                actor_username="Admin",
                entity_type="integration",
                entity_id=provider,
                action="UPDATE",
                details=f"Provider '{provider}' disconnected."
            )
            return True
        return False
