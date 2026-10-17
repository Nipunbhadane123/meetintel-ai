import os
import json
import logging
from fastapi import APIRouter, Request, Header, HTTPException, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from storage.database import get_db
from storage import repository
from integrations.zoom_service import ZoomIntegration
from integrations.google_workspace import GoogleWorkspaceIntegration
from integrations.email_service import EmailNotificationService
from integrations.manager import IntegrationCenterManager

logger = logging.getLogger(__name__)
router = APIRouter()

# ---------------------------------------------------------
# Zoom Webhooks & OAuth
# ---------------------------------------------------------

@router.post("/zoom/webhook")
async def zoom_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    x_zm_signature: str = Header(None),
    x_zm_request_timestamp: str = Header(None)
):
    """
    Receives and processes Zoom cloud recording webhooks.
    Includes HMAC-SHA256 signature verification and replay protection.
    """
    body_bytes = await request.body()
    zoom = ZoomIntegration()
    
    # 1. Signature Verification
    if x_zm_signature and x_zm_request_timestamp:
        is_valid = zoom.verify_webhook_signature(x_zm_request_timestamp, body_bytes, x_zm_signature)
        if not is_valid:
            logger.warning("Rejected Zoom webhook: Invalid HMAC signature or expired timestamp.")
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
            
    try:
        payload = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # 2. Endpoint URL Validation Challenge
    if payload.get("event") == "endpoint.url_validation":
        plain_token = payload.get("payload", {}).get("plainToken", "")
        return zoom.handle_endpoint_url_validation(plain_token)

    # 3. Process Event
    result = zoom.process_recording_webhook(db, payload)
    return result

# ---------------------------------------------------------
# Google Workspace OAuth & Webhooks
# ---------------------------------------------------------

@router.get("/google/oauth/callback")
def google_oauth_callback(
    code: str,
    state: str = None,
    db: Session = Depends(get_db)
):
    """Handles Google OAuth 2.0 authorization code return."""
    google = GoogleWorkspaceIntegration()
    result = google.exchange_code(db, code)
    if result.get("status") == "success":
        user_email = result.get("email", "Google Account")
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Google Workspace Connected | MeetIntel AI</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0E0F1E; color: #FFFFFF; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .card {{ background: #18192E; border: 1px solid rgba(108, 77, 255, 0.35); border-radius: 16px; padding: 2.5rem 3rem; text-align: center; max-width: 480px; box-shadow: 0 16px 40px rgba(0,0,0,0.5); }}
                h2 {{ color: #A78BFA; margin: 0 0 12px 0; font-size: 1.5rem; }}
                p {{ color: #94A3B8; font-size: 0.95rem; line-height: 1.5; margin: 0 0 1rem 0; }}
                .email {{ color: #FFFFFF; font-weight: 600; background: rgba(108,77,255,0.25); padding: 4px 10px; border-radius: 6px; }}
                .success-box {{ background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 14px; margin: 1.25rem 0; color: #34D399; font-size: 0.95rem; font-weight: 600; line-height: 1.4; }}
                .btn {{ display: inline-block; padding: 11px 24px; background: #6C4DFF; color: #FFFFFF; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 0.92rem; border: none; cursor: pointer; transition: background 0.2s; }}
                .btn:hover {{ background: #5536E8; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>✦ Google Workspace Connected!</h2>
                <p>Account <span class="email">{user_email}</span> is now securely connected.</p>
                <div class="success-box">
                    ✔ Setup Complete!<br>
                    Please close this tab and return to your MeetIntel AI tab.
                </div>
                <button class="btn" onclick="window.close();">Close This Tab</button>
            </div>
            <script>
                // Attempt automatic close after 3 seconds
                setTimeout(function() {{
                    try {{ window.close(); }} catch(e) {{}}
                }}, 3000);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html)
    raise HTTPException(status_code=400, detail=result.get("message", "OAuth failed"))

@router.post("/meet/webhook")
async def meet_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handles Google Drive / Meet push notifications for new recordings or transcripts."""
    logger.info("Received Google Meet push notification.")
    google = GoogleWorkspaceIntegration()
    # Query discovered artifacts and import any ready files
    discovered = google.discover_and_import_artifacts(db, user_id="system")
    return {"status": "accepted", "discovered_count": len(discovered)}

# ---------------------------------------------------------
# Integration Status & Actions
# ---------------------------------------------------------

@router.get("/integrations/status")
def get_integrations_status(db: Session = Depends(get_db)):
    """Returns the verified live status of all enterprise integrations."""
    manager = IntegrationCenterManager()
    return manager.get_all_integration_statuses(db)

@router.post("/integrations/{provider}/test")
def test_integration(provider: str, db: Session = Depends(get_db)):
    """Tests connection to the specified provider."""
    manager = IntegrationCenterManager()
    return manager.test_connection(db, provider)

@router.post("/notifications/{notification_id}/acknowledge")
def acknowledge_followup(notification_id: str, x_user_id: str = Header("admin"), db: Session = Depends(get_db)):
    """Allows an employee to acknowledge receipt of an absent meeting follow-up."""
    email_service = EmailNotificationService()
    success = email_service.acknowledge_notification(db, notification_id, user_id=x_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "acknowledged", "notification_id": notification_id}
