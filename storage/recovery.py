import os
import sys
import logging
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from storage.models import User, Organization
from storage.auth import hash_password
from storage import repository

logger = logging.getLogger(__name__)

WEAK_PASSWORDS = {
    "admin", "admin123", "password", "password123", "12345678",
    "your-secure-admin-password", "placeholder", "changeme", "change-me"
}

def recover_admin_account(
    db: Session,
    new_password: str,
    admin_username: str = "admin",
    admin_email: str = "admin@meetintel.ai",
    org_id: str = "org-default-001",
    operator_note: str = "Authorized Recovery Utility"
) -> User:
    """
    Secure, authorized recovery procedure for the MeetIntel AI administrator account.
    Verifies password policy, hashes using the project's standard PBKDF2 HMAC SHA-256 algorithm,
    safely updates or provisions the administrator account, and records an immutable audit log.
    Never prints or logs the raw password or password hash.
    """
    if not new_password or not isinstance(new_password, str):
        raise ValueError("Password cannot be empty.")
        
    trimmed_password = new_password.strip()
    if len(trimmed_password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
        
    clean_username = (admin_username or "admin").strip().lower()
    
    # Ensure default organization exists
    default_org = db.query(Organization).filter(Organization.id == org_id).first()
    if not default_org:
        default_org = Organization(
            id=org_id,
            name="Acme Global Technologies",
            domain="acmeglobal.io"
        )
        db.add(default_org)
        db.commit()

    # Find existing admin user (case-insensitive)
    admin = db.query(User).filter(func.lower(User.username) == clean_username).first()
    
    # Hash password using existing secure PBKDF2 salt:hash mechanism
    new_hashed_password = hash_password(trimmed_password)
    
    if admin:
        admin.hashed_password = new_hashed_password
        admin.role = "Admin"
        if not admin.org_id:
            admin.org_id = default_org.id
        if not admin.full_name:
            admin.full_name = "System Administrator"
        db.commit()
        db.refresh(admin)
        action_type = "UPDATE"
        details_msg = f"Administrator account '{admin.username}' credentials recovered via authorized procedure."
    else:
        admin = User(
            id=str(uuid.uuid4()),
            org_id=default_org.id,
            username=clean_username,
            email=admin_email,
            role="Admin",
            full_name="System Administrator",
            department="Operations",
            hashed_password=new_hashed_password
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        action_type = "CREATE"
        details_msg = f"Administrator account '{admin.username}' provisioned via authorized recovery procedure."

    # Record immutable audit event
    repository.log_audit_event(
        db,
        org_id=admin.org_id or org_id,
        user_id=admin.id,
        actor_username="Security Admin Recovery",
        entity_type="user",
        entity_id=admin.id,
        action=action_type,
        details=f"{details_msg} Note: {operator_note}"
    )
    
    logger.info(f"Administrator account '{admin.username}' credentials successfully updated. Audit event logged.")
    return admin
