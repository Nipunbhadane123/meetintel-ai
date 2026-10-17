#!/usr/bin/env python3
"""
MeetIntel AI — Secure Administrator Recovery CLI

Usage (Interactive):
    python scripts/admin_recovery.py

Usage (Non-Interactive / CI / Automated Deployments):
    RECOVERY_ADMIN_PASSWORD="YourStrongPassword123!" python scripts/admin_recovery.py --confirm
    or:
    python scripts/admin_recovery.py --password "YourStrongPassword123!" --confirm

Features:
- Never echoes input password to console or shell logs (uses getpass)
- Uses project's standard PBKDF2 HMAC SHA-256 (100k iterations, random 16B salt)
- Preserves all existing database records, meetings, tasks, and historical data
- Automatically records an immutable audit log entry
"""

import sys
import os
import argparse
import getpass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage.database import SessionLocal, init_db
from storage.recovery import recover_admin_account

def main():
    parser = argparse.ArgumentParser(description="Securely recover or reset the MeetIntel AI Administrator Account.")
    parser.add_argument("--password", help="New administrator password (prefer interactive input or RECOVERY_ADMIN_PASSWORD env var)", default=None)
    parser.add_argument("--confirm", action="store_true", help="Confirm non-interactive execution")
    parser.add_argument("--username", default="admin", help="Administrator username (default: admin)")
    parser.add_argument("--email", default="admin@meetintel.ai", help="Administrator email (default: admin@meetintel.ai)")
    
    args = parser.parse_args()

    # Determine password
    new_password = args.password or os.getenv("RECOVERY_ADMIN_PASSWORD")

    if not new_password:
        # Interactive mode
        print("\n=======================================================")
        print("  MeetIntel AI — Secure Administrator Account Recovery")
        print("=======================================================\n")
        print("This utility will set a new password for the administrator account.")
        print("Existing database records, meetings, and projects are strictly preserved.\n")

        try:
            pwd1 = getpass.getpass("Enter new administrator password: ")
            if not pwd1 or len(pwd1.strip()) < 8:
                print("\n[ERROR] Password must be at least 8 characters long.")
                sys.exit(1)
                
            pwd2 = getpass.getpass("Confirm new administrator password: ")
            if pwd1 != pwd2:
                print("\n[ERROR] Passwords do not match. Aborting.")
                sys.exit(1)
                
            new_password = pwd1
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(1)
    else:
        if not args.confirm:
            print("[ERROR] Non-interactive mode requires the --confirm flag.")
            sys.exit(1)

    # Validate length
    if len(new_password.strip()) < 8:
        print("[ERROR] Password must be at least 8 characters long.")
        sys.exit(1)

    # Initialize DB schema safely
    init_db()

    db = SessionLocal()
    try:
        admin = recover_admin_account(
            db=db,
            new_password=new_password,
            admin_username=args.username,
            admin_email=args.email,
            operator_note="CLI recovery execution"
        )
        print("\n-------------------------------------------------------")
        print(f" [SUCCESS] Administrator account '{admin.username}' recovered successfully!")
        print(f" User ID: {admin.id}")
        print(f" Role:    {admin.role}")
        print(f" Email:   {admin.email}")
        print(f" Org ID:  {admin.org_id}")
        print(" Audit log record created.")
        print("-------------------------------------------------------\n")
    except Exception as e:
        print(f"\n[ERROR] Administrator recovery failed: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
