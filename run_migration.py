from storage.database import init_db, SessionLocal
from storage.models import User, Meeting
from storage.auth import hash_password
import uuid

def migrate():
    # Create tables
    init_db()
    
    db = SessionLocal()
    
    # Check if admin user exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Creating admin user...")
        admin = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@meetintel.ai",
            hashed_password=hash_password("admin123")
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    
    # Migrate meetings without a user
    meetings = db.query(Meeting).filter(Meeting.user_id == None).all()
    if meetings:
        print(f"Migrating {len(meetings)} meetings to admin user...")
        for m in meetings:
            m.user_id = admin.id
        db.commit()
    print("Migration complete.")
    db.close()

if __name__ == "__main__":
    migrate()
