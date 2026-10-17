import os
import hmac
import hashlib
import time
import json
import logging
from typing import Dict, Any, Optional
import requests
from sqlalchemy.orm import Session

from .crypto import encrypt_token, decrypt_token
from storage import repository, models

logger = logging.getLogger(__name__)

ZOOM_OAUTH_URL = "https://zoom.us/oauth/authorize"
ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API_BASE = "https://api.zoom.us/v2"

class ZoomIntegration:
    def __init__(self, org_id: str = "org-default-001"):
        self.org_id = org_id
        self.client_id = os.getenv("ZOOM_CLIENT_ID", "")
        self.client_secret = os.getenv("ZOOM_CLIENT_SECRET", "")
        self.webhook_secret = os.getenv("ZOOM_WEBHOOK_SECRET", "")
        self.redirect_uri = os.getenv("ZOOM_REDIRECT_URI", "http://localhost:8501/api/zoom/oauth/callback")
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true" or not (self.client_id and self.client_secret)

    def is_configured(self) -> bool:
        """Returns True if real client credentials are set in environment."""
        return bool(self.client_id and self.client_secret)

    def get_auth_url(self, state: str = "meetintel_zoom_state") -> str:
        """Generates Zoom OAuth 2.0 authorization URL."""
        if not self.is_configured():
            return f"mock://zoom-oauth?state={state}&mode=demo"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state
        }
        import urllib.parse
        return f"{ZOOM_OAUTH_URL}?{urllib.parse.urlencode(params)}"

    def verify_webhook_signature(self, timestamp: str, body_bytes: bytes, signature_header: str) -> bool:
        """
        Validates Zoom webhook HMAC-SHA256 signature to prevent replay and forgery attacks.
        v0={hash of v0:timestamp:body}
        """
        if self.demo_mode or not self.webhook_secret:
            # In demo mode without secret, accept if test header present or mock
            return signature_header.startswith("v0=") or signature_header == "mock_signature"
            
        try:
            # Replay protection: check timestamp is within 5 minutes (300 seconds)
            current_ts = int(time.time())
            msg_ts = int(timestamp)
            if abs(current_ts - msg_ts) > 300:
                logger.warning(f"Zoom webhook timestamp verification failed: expired by {abs(current_ts - msg_ts)}s")
                return False

            message = f"v0:{timestamp}:".encode('utf-8') + body_bytes
            expected_hash = hmac.new(
                self.webhook_secret.encode('utf-8'),
                message,
                hashlib.sha256
            ).hexdigest()
            expected_sig = f"v0={expected_hash}"

            return hmac.compare_digest(expected_sig, signature_header)
        except Exception as e:
            logger.error(f"Error validating Zoom webhook signature: {e}")
            return False

    def handle_endpoint_url_validation(self, plain_token: str) -> Dict[str, str]:
        """Handles Zoom webhook challenge validation response."""
        secret = self.webhook_secret or "mock_secret_for_demo"
        encrypted_token = hmac.new(
            secret.encode("utf-8"),
            plain_token.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return {"plainToken": plain_token, "encryptedToken": encrypted_token}

    def process_recording_webhook(self, db: Session, payload: dict) -> Dict[str, Any]:
        """
        Processes 'recording.completed' event safely:
        1. Checks for duplicate recording
        2. Respects Zoom plan (checks for cloud recording download access)
        3. Enqueues background job for audio download and transcription
        """
        event = payload.get("event")
        if event != "recording.completed":
            return {"status": "ignored", "reason": f"Unhandled event {event}"}

        meeting_obj = payload.get("payload", {}).get("object", {})
        meeting_uuid = meeting_obj.get("uuid", "mock_uuid")
        meeting_topic = meeting_obj.get("topic", "Zoom Meeting")
        download_token = payload.get("download_token", "")
        
        # Check duplicate protection
        existing_meeting = repository.get_meeting_by_external_id(db, external_id=meeting_uuid, source_platform="zoom", org_id=self.org_id)
        if existing_meeting:
            logger.info(f"Duplicate Zoom recording skipped: {meeting_uuid}")
            return {"status": "skipped", "reason": "Already imported"}

        # Check cloud recording files
        recording_files = meeting_obj.get("recording_files", [])
        audio_file = None
        for f in recording_files:
            if f.get("file_type") in ["M4A", "MP4"]:
                audio_file = f
                break

        conn = repository.get_integration_connection(db, provider="zoom", org_id=self.org_id)
        if self.demo_mode or (conn and conn.connection_status.endswith("(Demo)")):
            # Create simulated meeting record
            admin_user = db.query(models.User).filter(models.User.org_id == self.org_id).first()
            user_id = admin_user.id if admin_user else "admin"
            
            meeting = repository.create_meeting(
                db,
                filename=f"Zoom_{meeting_topic.replace(' ', '_')}.m4a",
                user_id=user_id,
                duration=meeting_obj.get("duration", 45.0) * 60,
                org_id=self.org_id,
                source_platform="zoom",
                external_meeting_id=meeting_uuid
            )
            repository.update_meeting_status(db, meeting.id, "Processing")
            
            # Enqueue background job
            repository.enqueue_job(
                db,
                job_type="process_meeting_artifact",
                payload={"meeting_id": meeting.id, "source": "zoom", "mock": True},
                org_id=self.org_id,
                idempotency_key=f"zoom_proc_{meeting_uuid}"
            )
            
            repository.upsert_integration_connection(
                db,
                provider="zoom",
                connection_status=conn.connection_status if conn else "Connected (Demo)",
                org_id=self.org_id,
                last_import_result=f"Imported meeting '{meeting_topic}' ({meeting_uuid[:8]})"
            )
            return {"status": "accepted", "mode": "demo", "meeting_id": meeting.id}

        # Real plan validation
        if not download_token:
            return {
                "status": "error",
                "message": "Zoom cloud recording download token missing. Please ensure your Zoom plan supports Cloud Recording."
            }

        # Real processing would enqueue download
        admin_user = db.query(models.User).filter(models.User.org_id == self.org_id).first()
        meeting = repository.create_meeting(
            db,
            filename=f"Zoom_{meeting_topic.replace(' ', '_')}.m4a",
            user_id=admin_user.id if admin_user else "admin",
            duration=meeting_obj.get("duration", 30.0) * 60,
            org_id=self.org_id,
            source_platform="zoom",
            external_meeting_id=meeting_uuid
        )
        repository.enqueue_job(
            db,
            job_type="process_meeting_artifact",
            payload={"meeting_id": meeting.id, "download_url": audio_file.get("download_url") if audio_file else None, "download_token": download_token},
            org_id=self.org_id,
            idempotency_key=f"zoom_proc_{meeting_uuid}"
        )
        return {"status": "accepted", "mode": "live", "meeting_id": meeting.id}
