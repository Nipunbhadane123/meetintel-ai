import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the SQLite database
DATABASE_URL = "sqlite:///meetintel.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Safe schema migration for SQLite
    import sqlite3
    db_path = DATABASE_URL.replace("sqlite:///", "")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user_id exists in meetings table
        cursor.execute("PRAGMA table_info(meetings)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "user_id" not in columns:
            print("Migrating schema: Adding user_id to meetings table...")
            cursor.execute("ALTER TABLE meetings ADD COLUMN user_id VARCHAR REFERENCES users(id)")
            conn.commit()
            
        # Check if theme_preference exists in users table
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [info[1] for info in cursor.fetchall()]
        if "theme_preference" not in user_columns:
            print("Migrating schema: Adding theme_preference to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN theme_preference VARCHAR DEFAULT 'System'")
            conn.commit()
            
    except Exception as e:
        print(f"Schema migration error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

    # Auto-migrate meetings to a default admin user if they have no owner
    db = SessionLocal()
    try:
        from .models import User, Meeting
        from .auth import hash_password
        import uuid
        
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
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
    except Exception as e:
        print(f"Data migration error: {e}")
        db.rollback()
    finally:
        db.close()
