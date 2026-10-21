import os
os.environ["GEMINI_API_KEY"] = "mock_key"

import pytest
from fastapi.testclient import TestClient
from api.main import app
from storage.database import init_db

init_db()

client = TestClient(app)
API_KEY = "dev-secret-key"
HEADERS = {"X-API-Key": API_KEY, "x-user-id": "test-user-id"}

def test_list_meetings():
    response = client.get("/meetings", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search():
    response = client.post("/search", json={"query": "test query"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

from unittest.mock import patch

@patch('ai.meeting_analyzer.MeetingAnalyzer.rag_ask')
def test_ask(mock_rag_ask):
    mock_rag_ask.return_value = {"answer": "Mocked answer", "sources": []}
    response = client.post("/ask", json={"question": "what is this?"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Mocked answer"

def test_auth_failure():
    response = client.get("/meetings", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403

def test_roi_endpoint_not_found():
    response = client.get("/meetings/non-existent-id-999/roi", headers=HEADERS)
    assert response.status_code == 404

def test_export_slack_not_found():
    response = client.post("/meetings/non-existent-id-999/export/slack", headers=HEADERS)
    assert response.status_code == 404

