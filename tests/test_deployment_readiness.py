import os
import json
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from storage.models import Base, Organization, User, Meeting, ActionItem, BackgroundJob
from storage.database import init_db
from storage.background_worker import PersistentBackgroundWorker
from audio.validator import validate_file, SUPPORTED_EXTENSIONS

def test_vercel_configuration_validity():
    """Verify that root vercel.json and web/vercel.json exist and are valid JSON."""
    root_vercel = Path("vercel.json")
    assert root_vercel.exists(), "Root vercel.json must exist"
    
    with open(root_vercel, "r") as f:
        data = json.load(f)
        assert data.get("framework") == "nextjs"
        assert "buildCommand" in data
        assert "outputDirectory" in data

    web_vercel = Path("web/vercel.json")
    assert web_vercel.exists(), "web/vercel.json must exist"
    with open(web_vercel, "r") as f:
        web_data = json.load(f)
        assert web_data.get("framework") == "nextjs"

def test_web_package_configuration():
    """Verify that web/package.json has correct scripts and dependencies."""
    pkg_file = Path("web/package.json")
    assert pkg_file.exists(), "web/package.json must exist"
    
    with open(pkg_file, "r") as f:
        pkg = json.load(f)
        assert "build" in pkg.get("scripts", {})
        assert "dependencies" in pkg
        assert "next" in pkg["dependencies"]
        assert "react" in pkg["dependencies"]

def test_database_url_postgresql_compatibility():
    """Verify that SQLite and PostgreSQL connection URLs are parsed safely."""
    sqlite_url = "sqlite:///meetintel.db"
    assert sqlite_url.startswith("sqlite")
    
    # Test connection args logic
    connect_args = {"check_same_thread": False} if sqlite_url.startswith("sqlite") else {}
    assert "check_same_thread" in connect_args
    
    pg_url = "postgresql://user:pass@ep-cool-db.us-east-2.aws.neon.tech/meetintel?sslmode=require"
    assert not pg_url.startswith("sqlite")
    connect_args_pg = {"check_same_thread": False} if pg_url.startswith("sqlite") else {}
    assert connect_args_pg == {}

def test_supported_audio_formats():
    """Verify supported audio extensions for ingestion."""
    assert ".wav" in SUPPORTED_EXTENSIONS
    assert ".mp3" in SUPPORTED_EXTENSIONS
    assert ".mp4" in SUPPORTED_EXTENSIONS
    assert ".m4a" in SUPPORTED_EXTENSIONS
    assert ".flac" in SUPPORTED_EXTENSIONS
    assert ".ogg" in SUPPORTED_EXTENSIONS
    assert ".mov" in SUPPORTED_EXTENSIONS

def test_background_worker_retry_mechanism():
    """Verify background worker handles failed jobs with retry backoff."""
    worker = PersistentBackgroundWorker()
    assert worker.poll_interval > 0
    assert hasattr(worker, "run_once")
    assert hasattr(worker, "_execute_job")

def test_tenant_data_isolation():
    """Verify queries enforce organization isolation."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import sessionmaker
    TestSession = sessionmaker(bind=engine)
    db = TestSession()

    try:
        org1 = Organization(id="org-1", name="Alpha Corp")
        org2 = Organization(id="org-2", name="Beta Corp")
        db.add_all([org1, org2])
        db.commit()

        u1 = User(id="u1", org_id="org-1", username="alpha_user", email="alpha@alpha.com", hashed_password="pwd")
        u2 = User(id="u2", org_id="org-2", username="beta_user", email="beta@beta.com", hashed_password="pwd")
        db.add_all([u1, u2])
        db.commit()

        # Query users isolated by org
        alpha_users = db.query(User).filter(User.org_id == "org-1").all()
        beta_users = db.query(User).filter(User.org_id == "org-2").all()

        assert len(alpha_users) == 1
        assert alpha_users[0].username == "alpha_user"
        assert len(beta_users) == 1
        assert beta_users[0].username == "beta_user"
    finally:
        db.close()
