import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from storage.database import get_db, init_db
from storage.models import Meeting
from storage.repository import get_meeting
from ai.meeting_analyzer import MeetingAnalyzer
from storage.knowledge import get_knowledge_repository
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Very simple Auth for the API since it didn't exist
API_KEY = os.getenv("API_KEY", "dev-secret-key")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="MeetIntel AI API", lifespan=lifespan)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5
    meeting_id: Optional[str] = None

class AskQuery(BaseModel):
    question: str
    meeting_id: Optional[str] = None

@app.get("/meetings")
def list_meetings(db = Depends(get_db), api_key: str = Depends(get_api_key)):
    meetings = db.query(Meeting).order_by(Meeting.date.desc()).all()
    return [{
        "id": m.id,
        "title": m.title,
        "date": m.date,
        "status": m.processing_status
    } for m in meetings]

@app.get("/meetings/{meeting_id}")
def get_meeting_detail(meeting_id: str, db = Depends(get_db), api_key: str = Depends(get_api_key)):
    m = get_meeting(db, meeting_id)
    if not m:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "id": m.id,
        "title": m.title,
        "date": m.date,
        "executive_summary": m.executive_summary,
        "key_points": m.key_points,
        "decisions": [{"id": d.id, "decision": d.decision} for d in m.decisions],
        "action_items": [{"id": a.id, "task": a.task, "assigned_to": a.assigned_to, "status": a.status} for a in m.action_items]
    }

@app.post("/search")
def search_knowledge(req: SearchQuery, api_key: str = Depends(get_api_key)):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    repo = get_knowledge_repository()
    try:
        t0 = time.time()
        results = repo.semantic_search(req.query, top_k=req.top_k, meeting_id=req.meeting_id)
        
        # Format the output slightly if needed
        return {
            "query": req.query,
            "results": results.get("results", []),
            "search_time_ms": results.get("search_time_ms", int((time.time() - t0) * 1000))
        }
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during search")

@app.post("/ask")
def ask_knowledge(req: AskQuery, api_key: str = Depends(get_api_key)):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    analyzer = MeetingAnalyzer()
    try:
        t0 = time.time()
        response = analyzer.rag_ask(req.question, meeting_id=req.meeting_id)
        
        # Check if the model failed or timed out based on known fallback
        if "I couldn't find this information" in response.get("answer", ""):
            # We still return 200, as it's a valid RAG response
            pass
            
        return {
            "question": req.question,
            "answer": response.get("answer", ""),
            "sources": response.get("sources", []),
            "generation_time_ms": int((time.time() - t0) * 1000)
        }
    except Exception as e:
        logger.error(f"RAG failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during ask")

