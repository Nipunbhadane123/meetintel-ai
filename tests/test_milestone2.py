import pytest
import json
from unittest.mock import MagicMock, patch
from ai.gemini import GeminiProvider
from ai.schemas import MeetingInsightsSchema
from ai.meeting_analyzer import MeetingAnalyzer
from storage.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.models import Meeting, ActionItem, Decision, Participant, Deadline, Priority

# Create a test database
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

SAMPLE_MOCK_JSON = """
{
    "summary": "The team discussed the mobile application launch and assigned API integration and UI testing responsibilities.",
    "key_points": ["Mobile application launch", "API integration", "UI testing"],
    "decisions": [
        {"decision": "Continue with launch", "context": "Discussed timeline", "timestamp_approx": null}
    ],
    "action_items": [
        {"task": "Complete API integration", "assigned_to": "Ravi", "deadline": "Friday", "priority": "High", "status": "Pending"},
        {"task": "Prepare UI testing report", "assigned_to": "Priya", "deadline": "Friday", "priority": "Medium", "status": "Pending"}
    ],
    "participants": [
        {"name": "Ravi", "speaker_id": "SPEAKER_01", "responsibilities": ["Complete API integration"]},
        {"name": "Priya", "speaker_id": "SPEAKER_02", "responsibilities": ["Prepare UI testing report"]},
        {"name": "Unknown Participant", "speaker_id": "SPEAKER_03", "responsibilities": []}
    ],
    "deadlines": [
        {"description": "API integration deadline", "date": "Friday", "related_task": "Complete API integration"}
    ],
    "priorities": [
        {"item": "API integration", "priority": "High"}
    ],
    "executive_summary": null,
    "meeting_objective": null,
    "meeting_type": null,
    "emotional_analysis": "Neutral",
    "key_topics": [],
    "risks": [],
    "recommendations": [],
    "next_steps": [],
    "meeting_plan": null
}
"""

@pytest.fixture
def mock_gemini():
    with patch('ai.gemini.genai.Client') as MockClient:
        # Mock client setup
        mock_instance = MagicMock()
        MockClient.return_value = mock_instance
        
        # Mock generate_content response
        mock_response = MagicMock()
        mock_response.text = SAMPLE_MOCK_JSON
        mock_instance.models.generate_content.return_value = mock_response
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            provider = GeminiProvider()
            yield provider, mock_instance

def test_input_validation(mock_gemini):
    provider, _ = mock_gemini
    with pytest.raises(ValueError, match="Transcript is empty"):
        provider.generate_insights("")

def test_output_parsing_and_schema_validation(mock_gemini):
    provider, _ = mock_gemini
    result = provider.generate_insights("dummy transcript")
    assert result["summary"] == "The team discussed the mobile application launch and assigned API integration and UI testing responsibilities."
    assert len(result["action_items"]) == 2
    assert result["action_items"][0]["assigned_to"] == "Ravi"

def test_malformed_json_handling(mock_gemini):
    provider, mock_instance = mock_gemini
    mock_response = MagicMock()
    mock_response.text = "NOT JSON"
    mock_instance.models.generate_content.return_value = mock_response
    
    with pytest.raises(RuntimeError):
        provider.generate_insights("dummy")

def test_empty_transcript_handling(mock_gemini):
    provider, _ = mock_gemini
    with pytest.raises(ValueError):
        provider.generate_insights("   ")

def test_chunking_logic(mock_gemini):
    provider, mock_instance = mock_gemini
    provider.max_chunk_length = 50
    long_transcript = "A" * 60 + "\n" + "B" * 60
    chunks = provider._chunk_transcript(long_transcript)
    assert len(chunks) > 1

def test_db_persistence():
    db = next(override_get_db())
    meeting = Meeting(id="test_meeting", title="Test")
    db.add(meeting)
    db.commit()
    
    ai = ActionItem(meeting_id="test_meeting", task="Task", assigned_to="Bob")
    p = Participant(meeting_id="test_meeting", name="Bob", speaker_id="SPK_1")
    db.add(ai)
    db.add(p)
    db.commit()
    
    retrieved = db.query(Participant).filter(Participant.name == "Bob").first()
    assert retrieved.speaker_id == "SPK_1"
    
    ai_retrieved = db.query(ActionItem).filter(ActionItem.assigned_to == "Bob").first()
    assert ai_retrieved.task == "Task"

