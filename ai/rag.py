import logging
import time
import os
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from storage.knowledge import get_knowledge_repository
from storage.database import get_db, SessionLocal
from storage.models import Meeting, ActionItem, Decision
from ai.meeting_analyzer import get_ai_provider
from ai.gemini import TransientAIError

logger = logging.getLogger(__name__)

class RAGSource(BaseModel):
    meeting_id: str
    meeting_title: str
    date: str
    content_type: str
    excerpt: str

class RAGResponse(BaseModel):
    answer: str = Field(description="The grounded answer to the user's question.")
    confidence: str = Field(description="High, Medium, or Low")
    sources: List[RAGSource] = Field(description="The list of sources used to generate the answer.")

class QueryRouter:
    @staticmethod
    def classify(question: str) -> str:
        q_lower = question.lower()
        if "action" in q_lower or "task" in q_lower:
            return "DIRECT_DATABASE_ACTIONS"
        if "decid" in q_lower or "decision" in q_lower:
            return "DIRECT_DATABASE_DECISIONS"
        if "who" in q_lower and ("attend" in q_lower or "participant" in q_lower or "speaker" in q_lower):
            return "DIRECT_DATABASE_PARTICIPANTS"
        if "how many meeting" in q_lower:
            return "DIRECT_DATABASE_COUNT"
        if "last meet" in q_lower or "latest meet" in q_lower or "newest meet" in q_lower:
            return "DIRECT_DATABASE_LAST"
        if "longest meet" in q_lower or "largest meet" in q_lower or "biggest meet" in q_lower:
            return "DIRECT_DATABASE_LONGEST"
        return "SEMANTIC"

class RAGService:
    def __init__(self):
        self.repo = get_knowledge_repository()
        self.provider = get_ai_provider()

    def ask(self, question: str, user_id: Optional[str] = None, meeting_id: Optional[str] = None, org_id: Optional[str] = None) -> dict:
        logger.info(f"[RAG] Query received: {question}")
        start_time = time.time()
        
        mode = QueryRouter.classify(question)
        logger.info(f"[RAG] Query classification: {mode}")
        
        search_results = self.retrieve(question, mode, user_id=user_id, meeting_id=meeting_id, org_id=org_id)
        retrieval_time = time.time() - start_time
        
        chunks_retrieved = len(search_results.get("results", []))
        logger.info(f"[RAG] Retrieved {chunks_retrieved} relevant chunks")
        
        if not search_results["results"]:
            logger.info("[RAG] No relevant chunks found. Aborting Gemini request.")
            return {
                "question": question,
                "answer": "No relevant meeting information was found.",
                "sources": [],
                "retrieval_time_ms": int(retrieval_time * 1000),
                "generation_time_ms": 0,
                "status": "NO_RESULTS",
                "retrieval_success": True,
                "generation_success": False,
                "error_type": "no_context",
                "deterministic": False
            }
            
        context_str, sources = self.build_context(search_results["results"])
        logger.info(f"[RAG] Context built with {len(sources)} sources.")
        
        if mode.startswith("DIRECT_DATABASE"):
            # Return deterministic answer immediately!
            answer = "Based on meeting records:\n\n"
            if mode == "DIRECT_DATABASE_ACTIONS":
                answer += "\n".join([f"• {s['excerpt']}" for s in sources if s['content_type'] == 'action_item'])
            elif mode == "DIRECT_DATABASE_DECISIONS":
                answer += "\n".join([f"• {s['excerpt']}" for s in sources if s['content_type'] == 'decision'])
            else:
                answer += "\n\n".join([s['excerpt'] for s in sources])
            
            if not answer.strip() or answer.strip() == "Based on meeting records:":
                answer = "Based on meeting records, no relevant information was found."
                
            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "retrieval_time_ms": int(retrieval_time * 1000),
                "generation_time_ms": 0,
                "status": "SUCCESS",
                "retrieval_success": True,
                "generation_success": True,
                "error_type": None,
                "deterministic": True
            }
        
        try:
            logger.info("[RAG] AI provider request started")
            gen_start = time.time()
            
            validated_data = self.provider.rag_ask_question(context_str, question)
            
            answer = validated_data.get("answer", "")
            llm_sources = validated_data.get("sources", [])
            
            gen_time = time.time() - gen_start
            logger.info("[RAG] AI provider request succeeded")
            logger.info("[RAG] Sources validated")
            return {
                "question": question,
                "answer": answer,
                "sources": llm_sources if llm_sources else sources,
                "retrieval_time_ms": int(retrieval_time * 1000),
                "generation_time_ms": int(gen_time * 1000),
                "status": "SUCCESS",
                "retrieval_success": True,
                "generation_success": True,
                "error_type": None,
                "deterministic": False
            }
        except Exception as e:
            gen_time = time.time() - gen_start
            logger.error(f"[RAG] Generation failed: {e}")
            return {
                "question": question,
                "answer": "AI generation is temporarily unavailable. Please try again later.",
                "sources": sources,
                "retrieval_time_ms": int(retrieval_time * 1000),
                "generation_time_ms": int(gen_time * 1000),
                "status": "ERROR",
                "retrieval_success": True,
                "generation_success": False,
                "error_type": "GENERATION_ERROR",
                "deterministic": False
            }

    def _build_prompt(self, context: str, question: str) -> str:
        return f"""
You are MeetIntel AI's meeting knowledge assistant.

Answer the user's question using ONLY the supplied meeting context.
Do not use external knowledge.
Do not invent names, dates, deadlines, decisions, participants, actions, or events.
If the retrieved context does not contain enough information, clearly state that the information could not be found.
If multiple meetings are relevant, distinguish them.
Always identify the source meeting when possible.
For factual answers, preserve the meaning of the retrieved data.
Never fabricate an answer merely to satisfy the user.

RETRIEVED MEETING CONTEXT:
{context}

USER QUESTION:
{question}
"""

    def retrieve(self, question: str, mode: str, user_id: Optional[str] = None, meeting_id: Optional[str] = None, org_id: Optional[str] = None) -> dict:
        results = []
        db = SessionLocal()
        
        try:
            if mode == "DIRECT_DATABASE_LAST":
                query = db.query(Meeting)
                if org_id:
                    query = query.filter(Meeting.org_id == org_id)
                if user_id:
                    query = query.filter(Meeting.user_id == user_id)
                if meeting_id:
                    query = query.filter(Meeting.id == meeting_id)
                m = query.order_by(Meeting.date.desc()).first()
                if m:
                    results.append(self._format_meeting_meta(m))
            elif mode == "DIRECT_DATABASE_LONGEST":
                query = db.query(Meeting)
                if org_id:
                    query = query.filter(Meeting.org_id == org_id)
                if user_id:
                    query = query.filter(Meeting.user_id == user_id)
                if meeting_id:
                    query = query.filter(Meeting.id == meeting_id)
                m = query.order_by(Meeting.duration.desc()).first()
                if m:
                    results.append(self._format_meeting_meta(m))
            elif mode == "DIRECT_DATABASE_COUNT":
                query = db.query(Meeting)
                if org_id:
                    query = query.filter(Meeting.org_id == org_id)
                if user_id:
                    query = query.filter(Meeting.user_id == user_id)
                if meeting_id:
                    query = query.filter(Meeting.id == meeting_id)
                count = query.count()
                results.append({
                    "metadata": {
                        "meeting_id": meeting_id or "all",
                        "meeting_title": "Aggregate query",
                        "meeting_date": "",
                        "content_type": "metadata"
                    },
                    "content": f"There are a total of {count} meetings in the database.",
                    "similarity": 1.0
                })
            elif mode == "DIRECT_DATABASE_PARTICIPANTS":
                query = db.query(Meeting)
                if org_id:
                    query = query.filter(Meeting.org_id == org_id)
                if user_id:
                    query = query.filter(Meeting.user_id == user_id)
                if meeting_id:
                    query = query.filter(Meeting.id == meeting_id)
                meetings = query.all()
                for m in meetings:
                    if m.participants:
                        parts = [p.name for p in m.participants]
                        results.append({
                            "metadata": {
                                "meeting_id": m.id,
                                "meeting_title": m.title,
                                "meeting_date": str(m.date),
                                "content_type": "participant"
                            },
                            "content": f"Participants: {', '.join(parts)}",
                            "similarity": 1.0
                        })
            elif mode in ["DIRECT_DATABASE_ACTIONS", "DIRECT_DATABASE_DECISIONS"]:
                query = db.query(Meeting)
                if org_id:
                    query = query.filter(Meeting.org_id == org_id)
                if user_id:
                    query = query.filter(Meeting.user_id == user_id)
                if meeting_id:
                    query = query.filter(Meeting.id == meeting_id)
                meetings = query.order_by(Meeting.date.desc()).limit(10).all()
                for m in meetings:
                    if mode == "DIRECT_DATABASE_ACTIONS" and m.action_items:
                        for a in m.action_items:
                            results.append({
                                "metadata": {
                                    "meeting_id": m.id,
                                    "meeting_title": m.title,
                                    "meeting_date": str(m.date),
                                    "content_type": "action_item"
                                },
                                "content": f"Task: {a.task}. Assigned to: {a.assigned_to}. Deadline: {a.deadline}. Status: {a.status}",
                                "similarity": 1.0
                            })
                    if mode == "DIRECT_DATABASE_DECISIONS" and m.decisions:
                        for d in m.decisions:
                            results.append({
                                "metadata": {
                                    "meeting_id": m.id,
                                    "meeting_title": m.title,
                                    "meeting_date": str(m.date),
                                    "content_type": "decision"
                                },
                                "content": f"Decision: {d.decision}. Context: {d.context}",
                                "similarity": 1.0
                            })
            else:
                top_k = int(os.getenv("RAG_TOP_K", "15"))
                sem_results = self.repo.semantic_search(question, user_id=user_id, meeting_id=meeting_id, org_id=org_id, top_k=top_k)
                results.extend(sem_results.get("results", []))
                
        finally:
            db.close()
            
        unique_results = []
        seen = set()
        for r in results:
            content = r.get("content", "")
            if content not in seen:
                seen.add(content)
                unique_results.append(r)
                
        return {"results": unique_results}

    def _format_meeting_meta(self, m: Meeting) -> dict:
        content = f"Meeting '{m.title}' occurred on {m.date}. Duration: {m.duration} seconds."
        if m.executive_summary:
            content += f" Summary: {m.executive_summary}"
        
        # Include participant info so LLM can answer "who was the speaker"
        if m.participants:
            parts = [p.name for p in m.participants]
            content += f" Participants/Speakers: {', '.join(parts)}."
            
        return {
            "metadata": {
                "meeting_id": str(m.id),
                "meeting_title": m.title,
                "meeting_date": str(m.date),
                "content_type": "metadata"
            },
            "content": content,
            "similarity": 1.0
        }

    def build_context(self, retrieved_chunks: list) -> tuple[str, list]:
        context_parts = []
        sources = []
        for result in retrieved_chunks:
            meta = result.get("metadata", {})
            title = meta.get("meeting_title", "Unknown Meeting")
            date = meta.get("meeting_date", "")
            ctype = meta.get("content_type", "unknown")
            text = result.get("content", "")
            
            context_part = f"--- MEETING: {title} ({date}) | TYPE: {ctype} ---\n{text}\n"
            context_parts.append(context_part)
            
            sources.append({
                "meeting_id": str(meta.get("meeting_id", "")),
                "meeting_title": str(title),
                "date": str(date),
                "content_type": str(ctype),
                "excerpt": str(text)[:200]
            })
            
        return "\n".join(context_parts), sources
