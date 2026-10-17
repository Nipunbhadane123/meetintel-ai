import pytest
import datetime
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from storage.models import Base, Project, ActionItem, User, Organization
from storage import repository

@pytest.fixture
def isolated_db():
    """Provides a completely isolated, clean in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    # Pre-seed a test organization
    test_org = Organization(id="org-test-001", name="Acme Test Org")
    session.add(test_org)
    session.commit()
    
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

# ---------------------------------------------------------------------------
# Test 1: Creating a valid project with repository.create_project
# ---------------------------------------------------------------------------
def test_create_valid_project(isolated_db):
    target = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=45)
    project = repository.create_project(
        isolated_db,
        org_id="org-test-001",
        name="Platform Scalability Initiative",
        description="Optimize database queries and background workers for 10x scale.",
        status="Active",
        target_date=target
    )
    
    assert project is not None
    assert project.id is not None
    # Validate UUID structure
    uuid_obj = uuid.UUID(project.id)
    assert str(uuid_obj) == project.id
    assert project.name == "Platform Scalability Initiative"
    assert project.org_id == "org-test-001"
    assert project.status == "Active"
    assert project.created_at is not None

    # Verify query retrieval
    retrieved = repository.get_project_by_id(isolated_db, project.id)
    assert retrieved is not None
    assert retrieved.name == "Platform Scalability Initiative"

# ---------------------------------------------------------------------------
# Test 2: Project model auto-generates UUID primary key when omitted
# ---------------------------------------------------------------------------
def test_project_model_auto_generates_uuid_default(isolated_db):
    """Verifies that direct instantiation of Project without id produces a valid UUID and avoids NOT NULL errors."""
    project = Project(
        org_id="org-test-001",
        name="Direct Model Project",
        description="Testing model-level UUID default generator",
        status="Active"
    )
    # The default callable is invoked by SQLAlchemy upon add/flush
    isolated_db.add(project)
    isolated_db.commit()
    isolated_db.refresh(project)
    
    assert project.id is not None
    assert len(project.id) == 36
    assert uuid.UUID(project.id).version == 4

# ---------------------------------------------------------------------------
# Test 3: Rejecting invalid projects (empty or whitespace name)
# ---------------------------------------------------------------------------
def test_reject_empty_or_whitespace_name(isolated_db):
    with pytest.raises(ValueError, match="Project name is required and cannot be empty"):
        repository.create_project(isolated_db, org_id="org-test-001", name="")

    with pytest.raises(ValueError, match="Project name is required and cannot be empty"):
        repository.create_project(isolated_db, org_id="org-test-001", name="   \t\n  ")

    # Confirm no rows were written
    projects = repository.get_projects(isolated_db, org_id="org-test-001")
    assert len(projects) == 0

# ---------------------------------------------------------------------------
# Test 4: Database-level constraint rejection (null name)
# ---------------------------------------------------------------------------
def test_reject_null_name_at_db_level(isolated_db):
    project = Project(
        org_id="org-test-001",
        name=None
    )
    isolated_db.add(project)
    with pytest.raises(IntegrityError):
        isolated_db.commit()
        
    isolated_db.rollback()
    # Confirm rollback left the session in a healthy state
    projects = repository.get_projects(isolated_db, org_id="org-test-001")
    assert len(projects) == 0

# ---------------------------------------------------------------------------
# Test 5: Idempotent seeding prevents duplicate project creation
# ---------------------------------------------------------------------------
def test_idempotent_seeding_prevents_duplicates(isolated_db):
    # First seed invocation
    first_run = repository.seed_default_projects(isolated_db, org_id="org-test-001")
    assert len(first_run) == 3
    initial_ids = {p.id for p in first_run}
    assert len(initial_ids) == 3

    # All 3 exist in DB
    all_projects = repository.get_projects(isolated_db, org_id="org-test-001")
    assert len(all_projects) == 3

    # Second seed invocation - must be fully idempotent
    second_run = repository.seed_default_projects(isolated_db, org_id="org-test-001")
    assert len(second_run) == 3
    second_ids = {p.id for p in second_run}
    
    # IDs and total counts must remain unchanged
    assert initial_ids == second_ids
    assert len(repository.get_projects(isolated_db, org_id="org-test-001")) == 3

# ---------------------------------------------------------------------------
# Test 6: Transaction rollback preserves session for subsequent operations
# ---------------------------------------------------------------------------
def test_transaction_rollback_preserves_session(isolated_db):
    # Trigger an intentional IntegrityError
    invalid_project = Project(name=None)
    isolated_db.add(invalid_project)
    
    with pytest.raises(IntegrityError):
        isolated_db.commit()
        
    # Crucial step: explicit rollback on transaction failure
    isolated_db.rollback()
    
    # Verify session is not poisoned (no PendingRollbackError)
    valid_project = repository.create_project(
        isolated_db,
        org_id="org-test-001",
        name="Resilient Project After Rollback",
        description="Session successfully recovered from rollback"
    )
    assert valid_project.id is not None
    assert valid_project.name == "Resilient Project After Rollback"
    
    # Verify query works normally
    all_projects = repository.get_projects(isolated_db, org_id="org-test-001")
    assert len(all_projects) == 1
    assert all_projects[0].name == "Resilient Project After Rollback"

# ---------------------------------------------------------------------------
# Test 7: Multi-tenant organizational isolation
# ---------------------------------------------------------------------------
def test_organization_isolation(isolated_db):
    repository.create_project(isolated_db, org_id="org-alpha", name="Alpha Project")
    repository.create_project(isolated_db, org_id="org-beta", name="Beta Project 1")
    repository.create_project(isolated_db, org_id="org-beta", name="Beta Project 2")
    
    alpha_projects = repository.get_projects(isolated_db, org_id="org-alpha")
    beta_projects = repository.get_projects(isolated_db, org_id="org-beta")
    
    assert len(alpha_projects) == 1
    assert alpha_projects[0].name == "Alpha Project"
    
    assert len(beta_projects) == 2
    assert {p.name for p in beta_projects} == {"Beta Project 1", "Beta Project 2"}

# ---------------------------------------------------------------------------
# Test 8: Project to ActionItem relationship integrity
# ---------------------------------------------------------------------------
def test_project_action_item_relationship(isolated_db):
    project = repository.create_project(
        isolated_db,
        org_id="org-test-001",
        name="Security Audit & Compliance"
    )
    
    action_item = ActionItem(
        org_id="org-test-001",
        project_id=project.id,
        task="Conduct external penetration testing",
        status="Pending",
        priority="High"
    )
    isolated_db.add(action_item)
    isolated_db.commit()
    
    # Query tasks linked to this project
    linked_tasks = isolated_db.query(ActionItem).filter(
        ActionItem.project_id == project.id
    ).all()
    
    assert len(linked_tasks) == 1
    assert linked_tasks[0].task == "Conduct external penetration testing"
    assert linked_tasks[0].project_id == project.id
