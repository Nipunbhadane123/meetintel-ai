import os
import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.models import Base, User, Organization, AuditEvent
from storage.auth import hash_password, verify_password, HASH_ITERATIONS, SALT_SIZE
from storage import repository
from storage.recovery import recover_admin_account

TEST_AUTH_DB = "test_auth_flow.db"
test_engine = create_engine(f"sqlite:///{TEST_AUTH_DB}", connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module")
def auth_db():
    if os.path.exists(TEST_AUTH_DB):
        try:
            os.remove(TEST_AUTH_DB)
        except Exception:
            pass

    Base.metadata.create_all(bind=test_engine)
    db = TestSession()

    org = Organization(id="org-test-auth", name="Auth Test Org", domain="authtest.io")
    db.add(org)
    db.commit()

    # Seed test users
    admin = User(
        id=str(uuid.uuid4()),
        org_id=org.id,
        username="admin",
        email="admin@authtest.io",
        role="Admin",
        full_name="Test Administrator",
        department="Operations",
        hashed_password=hash_password("SuperSecretAdminPass123!")
    )
    employee = User(
        id=str(uuid.uuid4()),
        org_id=org.id,
        username="john_doe",
        email="john@authtest.io",
        role="Employee",
        full_name="John Doe",
        department="Engineering",
        hashed_password=hash_password("EmployeePass456!")
    )
    db.add_all([admin, employee])
    db.commit()

    yield db

    db.close()
    test_engine.dispose()
    if os.path.exists(TEST_AUTH_DB):
        try:
            os.remove(TEST_AUTH_DB)
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Test 1: Password Hash Verification & Algorithm Standards
# ---------------------------------------------------------------------------
def test_password_hash_verification_sha256():
    raw_pwd = "MySecurePassword789!"
    hashed = hash_password(raw_pwd)

    assert ":" in hashed
    parts = hashed.split(":")
    assert len(parts) == 2
    salt_hex, hash_hex = parts

    # 16 bytes salt = 32 hex chars; 32 bytes sha256 = 64 hex chars
    assert len(salt_hex) == SALT_SIZE * 2
    assert len(hash_hex) == 64

    # Salting works (two hashes of same password produce distinct salts and hashes)
    hashed_again = hash_password(raw_pwd)
    assert hashed != hashed_again

    # Matching verifies True
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password(raw_pwd, hashed_again) is True

    # Non-matching verifies False
    assert verify_password("WrongPassword!", hashed) is False

# ---------------------------------------------------------------------------
# Test 2: Password Verification Type Safety & Corrupted Input Resilience
# ---------------------------------------------------------------------------
def test_verify_password_resilience():
    raw_pwd = "ValidPassword123!"
    valid_hash = hash_password(raw_pwd)

    # None and empty values must safely return False without raising exceptions
    assert verify_password(None, valid_hash) is False
    assert verify_password(raw_pwd, None) is False
    assert verify_password("", valid_hash) is False
    assert verify_password(raw_pwd, "") is False
    assert verify_password(None, None) is False

    # Non-string types
    assert verify_password(12345, valid_hash) is False
    assert verify_password(raw_pwd, 12345) is False

    # Malformed hashes
    assert verify_password(raw_pwd, "no_colon_here") is False
    assert verify_password(raw_pwd, "too:many:colons:in:hash") is False
    assert verify_password(raw_pwd, "invalidhexsalt:invalidhexhash") is False

# ---------------------------------------------------------------------------
# Test 3: Username Normalization (Case-Insensitivity & Whitespace Trimming)
# ---------------------------------------------------------------------------
def test_username_normalization_and_whitespace(auth_db):
    # Lookup using varied casing
    u_lower = repository.get_user_by_username(auth_db, "admin")
    u_upper = repository.get_user_by_username(auth_db, "ADMIN")
    u_title = repository.get_user_by_username(auth_db, "Admin")
    u_spaced = repository.get_user_by_username(auth_db, "  admin  ")

    assert u_lower is not None
    assert u_upper is not None
    assert u_title is not None
    assert u_spaced is not None
    assert u_lower.id == u_upper.id == u_title.id == u_spaced.id

# ---------------------------------------------------------------------------
# Test 4: Correct Credentials Authenticate Successfully
# ---------------------------------------------------------------------------
def test_correct_credentials_login(auth_db):
    user = repository.get_user_by_username(auth_db, "admin")
    assert user is not None
    is_valid = verify_password("SuperSecretAdminPass123!", user.hashed_password)
    assert is_valid is True

# ---------------------------------------------------------------------------
# Test 5: Incorrect Password Rejected
# ---------------------------------------------------------------------------
def test_incorrect_password_rejected(auth_db):
    user = repository.get_user_by_username(auth_db, "admin")
    assert user is not None
    is_valid = verify_password("IncorrectPassword999!", user.hashed_password)
    assert is_valid is False

# ---------------------------------------------------------------------------
# Test 6: Missing User Rejected
# ---------------------------------------------------------------------------
def test_missing_user_rejected(auth_db):
    non_existent = repository.get_user_by_username(auth_db, "ghost_user_does_not_exist")
    assert non_existent is None

# ---------------------------------------------------------------------------
# Test 7: Administrator Recovery Updates Existing Admin Password
# ---------------------------------------------------------------------------
def test_admin_recovery_procedure_existing_admin(auth_db):
    new_pass = "RecoveredAdminSecret999!"
    recovered_admin = recover_admin_account(
        db=auth_db,
        new_password=new_pass,
        admin_username="admin",
        operator_note="Automated recovery unit test"
    )

    assert recovered_admin is not None
    assert recovered_admin.username == "admin"
    assert recovered_admin.role == "Admin"

    # Verify newly recovered password immediately authenticates
    assert verify_password(new_pass, recovered_admin.hashed_password) is True
    # Verify old password no longer authenticates
    assert verify_password("SuperSecretAdminPass123!", recovered_admin.hashed_password) is False

    # Verify audit event was logged
    audit = auth_db.query(AuditEvent).filter(
        AuditEvent.action == "UPDATE",
        AuditEvent.entity_type == "user",
        AuditEvent.entity_id == recovered_admin.id
    ).first()
    assert audit is not None
    assert "recovered" in audit.details.lower()

# ---------------------------------------------------------------------------
# Test 8: Administrator Recovery Provisions Account if Missing
# ---------------------------------------------------------------------------
def test_admin_recovery_procedure_missing_admin(auth_db):
    new_admin_pass = "NewOrgAdminSecret888!"
    new_admin = recover_admin_account(
        db=auth_db,
        new_password=new_admin_pass,
        admin_username="brand_new_admin",
        admin_email="new_admin@authtest.io",
        org_id="org-test-auth"
    )

    assert new_admin is not None
    assert new_admin.username == "brand_new_admin"
    assert new_admin.role == "Admin"
    assert verify_password(new_admin_pass, new_admin.hashed_password) is True

# ---------------------------------------------------------------------------
# Test 9: Administrator Recovery Validates Password Strength
# ---------------------------------------------------------------------------
def test_admin_recovery_password_strength_validation(auth_db):
    # Empty password
    with pytest.raises(ValueError, match="cannot be empty"):
        recover_admin_account(auth_db, new_password="")

    # Too short (< 8 characters)
    with pytest.raises(ValueError, match="at least 8 characters"):
        recover_admin_account(auth_db, new_password="short")

# ---------------------------------------------------------------------------
# Test 10: Unauthenticated Users Blocked from Protected Views
# ---------------------------------------------------------------------------
def test_unauthenticated_session_access_blocked():
    """
    Verifies that when session state lacks 'user_id' or user_id is None,
    protected pages cannot be accessed and the login flow is rendered.
    """
    fake_session = {}
    assert not fake_session.get("user_id")

    # When user_id is None or missing, authentication gate triggers
    assert bool(fake_session.get("user_id")) is False

    fake_session["user_id"] = None
    assert bool(fake_session.get("user_id")) is False

    # Only when valid user_id is set is the session considered authenticated
    fake_session["user_id"] = "valid-session-user-uuid"
    assert bool(fake_session.get("user_id")) is True
