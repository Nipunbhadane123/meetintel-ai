from dotenv import load_dotenv
load_dotenv()
import pytest
import os
from ai.meeting_analyzer import MeetingAnalyzer

SAMPLE_TRANSCRIPT = """
Good morning everyone.

Today we discussed the mobile application launch.

Ravi will complete the API integration by Friday.

Priya will prepare the UI testing report by Friday.

The team decided to continue with the planned mobile application launch.

The API integration is high priority.

The UI testing report is medium priority.

Thank you.
"""

@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="Requires GEMINI_API_KEY")
def test_full_pipeline_with_real_llm():
    analyzer = MeetingAnalyzer()
    
    # Run analysis
    result = analyzer.analyze(SAMPLE_TRANSCRIPT)
    
    # Check Summary
    assert "mobile application" in result["summary"].lower()
    
    # Check Decisions
    assert any("continue" in d["decision"].lower() for d in result["decisions"])
    
    # Check Action Items
    assert len(result["action_items"]) >= 2
    tasks = [ai["task"].lower() for ai in result["action_items"]]
    assert any("api integration" in t for t in tasks)
    assert any("ui testing" in t for t in tasks)
    
    # Check Participants
    participants = [p["name"].lower() for p in result["participants"]]
    assert "ravi" in participants
    assert "priya" in participants
    
    # Check Deadlines
    assert len(result["deadlines"]) >= 1
    
    # Check Priorities
    assert len(result["priorities"]) >= 1
