import time
import logging
import uuid
from typing import List, Dict, Any, Optional

from storage.database import SessionLocal
from storage.repository import get_meeting
from storage.models import TranscriptSegment, Meeting
from storage.vector_store import VectorStore
from ai.embeddings import EmbeddingService, chunk_transcript, chunk_text, generate_content_hash

logger = logging.getLogger(__name__)

class KnowledgeRepository:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_service = EmbeddingService()
        
    def index_meeting(self, meeting_id: str) -> bool:
        """Extracts data from the relational database and indexes it in the vector store."""
        db = SessionLocal()
        try:
            meeting = get_meeting(db, meeting_id)
            if not meeting:
                logger.error(f"Meeting {meeting_id} not found for indexing.")
                return False
                
            logger.info(f"Indexing meeting: {meeting.title} ({meeting_id})")
            
            # Delete old vectors for this meeting to prevent duplicates
            self.vector_store.delete_meeting_vectors(meeting_id)
            
            ids = []
            documents = []
            metadatas = []
            
            # 1. Index Transcript
            segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).order_by(TranscriptSegment.start).all()
            if segments:
                seg_dicts = [{"start": s.start, "end": s.end, "speaker": s.speaker, "text": s.text} for s in segments]
                chunks = chunk_transcript(seg_dicts)
                
                for i, chunk in enumerate(chunks):
                    ids.append(f"{meeting_id}_transcript_{i}")
                    documents.append(chunk["text"])
                    metadatas.append({
                        "meeting_id": meeting_id,
                        "meeting_title": meeting.title or "Untitled",
                        "meeting_date": str(meeting.date) if meeting.date else "",
                        "content_type": "transcript",
                        "start_time": chunk["start"],
                        "end_time": chunk["end"],
                        "speakers": ",".join(chunk["speakers"]) if chunk.get("speakers") else "",
                        "content_hash": chunk["content_hash"]
                    })
                    
            # 2. Index Summary (Executive Summary)
            if meeting.executive_summary:
                chunks = chunk_text(meeting.executive_summary)
                for i, chunk in enumerate(chunks):
                    ids.append(f"{meeting_id}_summary_{i}")
                    documents.append(chunk["text"])
                    metadatas.append({
                        "meeting_id": meeting_id,
                        "meeting_title": meeting.title or "Untitled",
                        "meeting_date": str(meeting.date) if meeting.date else "",
                        "content_type": "summary",
                        "content_hash": chunk["content_hash"]
                    })
                    
            # 2.5 Index Additional Insights
            additional_insights = [
                ("objective", meeting.meeting_objective),
                ("plan", meeting.meeting_plan),
                ("emotional_tone", meeting.emotional_analysis),
                ("key_topics", meeting.key_topics),
                ("key_points", meeting.key_points),
                ("risks", meeting.risks),
                ("recommendations", meeting.recommendations),
                ("next_steps", meeting.next_steps),
            ]
            
            for insight_type, insight_text in additional_insights:
                if insight_text and insight_text.strip() and insight_text.strip() != "[]":
                    text = f"{insight_type.replace('_', ' ').title()}: {insight_text}"
                    ids.append(f"{meeting_id}_insight_{insight_type}")
                    documents.append(text)
                    metadatas.append({
                        "meeting_id": meeting_id,
                        "meeting_title": meeting.title or "Untitled",
                        "meeting_date": str(meeting.date) if meeting.date else "",
                        "content_type": "insight",
                        "content_hash": generate_content_hash(text)
                    })
                    
            # 3. Index Decisions, Action Items, etc. (Can be batched as insights)
            insight_texts = []
            if meeting.decisions:
                # Assuming decisions is a JSON string or similar, but models.py says String.
                # Actually in the existing code, it is mapped as a related model, wait, let me check models.py
                # models.py says decisions is a relationship to Decision
                pass 
                
            for decision in meeting.decisions:
                text = f"Decision: {decision.decision}. Context: {decision.context}"
                ids.append(f"{meeting_id}_decision_{decision.id}")
                documents.append(text)
                metadatas.append({
                    "meeting_id": meeting_id,
                    "meeting_title": meeting.title or "Untitled",
                    "meeting_date": str(meeting.date) if meeting.date else "",
                    "content_type": "decision",
                    "source_id": str(decision.id),
                    "content_hash": generate_content_hash(text)
                })
                
            for action_item in meeting.action_items:
                text = f"Action Item: {action_item.task}. Assigned to: {action_item.assigned_to}. Deadline: {action_item.deadline}. Status: {action_item.status}"
                ids.append(f"{meeting_id}_action_item_{action_item.id}")
                documents.append(text)
                metadatas.append({
                    "meeting_id": meeting_id,
                    "meeting_title": meeting.title or "Untitled",
                    "meeting_date": str(meeting.date) if meeting.date else "",
                    "content_type": "action_item",
                    "source_id": str(action_item.id),
                    "content_hash": generate_content_hash(text)
                })
                
            for participant in meeting.participants:
                text = f"Participant: {participant.name}. Responsibilities: {participant.responsibilities}"
                ids.append(f"{meeting_id}_participant_{participant.id}")
                documents.append(text)
                metadatas.append({
                    "meeting_id": meeting_id,
                    "meeting_title": meeting.title or "Untitled",
                    "meeting_date": str(meeting.date) if meeting.date else "",
                    "content_type": "participant",
                    "source_id": str(participant.id),
                    "content_hash": generate_content_hash(text)
                })
                
            for deadline in meeting.deadlines:
                text = f"Deadline: {deadline.description}. Date: {deadline.date}. Related Task: {deadline.related_task}"
                ids.append(f"{meeting_id}_deadline_{deadline.id}")
                documents.append(text)
                metadatas.append({
                    "meeting_id": meeting_id,
                    "meeting_title": meeting.title or "Untitled",
                    "meeting_date": str(meeting.date) if meeting.date else "",
                    "content_type": "deadline",
                    "source_id": str(deadline.id),
                    "content_hash": generate_content_hash(text)
                })
                
            if not documents:
                logger.warning(f"No content to index for meeting {meeting_id}")
                return True
                
            # Generate embeddings
            embeddings = self.embedding_service.generate_embeddings(documents)
            
            # Insert into Vector DB
            self.vector_store.insert_vectors(ids, embeddings, documents, metadatas)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to index meeting {meeting_id}: {e}", exc_info=True)
            return False
        finally:
            db.close()
            
    def delete_meeting(self, meeting_id: str):
        """Removes a meeting from the vector store."""
        try:
            self.vector_store.delete_meeting_vectors(meeting_id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete meeting {meeting_id} from vector store: {e}")
            return False
            
    def semantic_search(self, query: str, meeting_id: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
        """Performs a semantic search across meetings."""
        start_time = time.time()
        
        # 1. Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        embedding_time = time.time()
        
        # 2. Vector search
        results = self.vector_store.search(query_embedding, meeting_id=meeting_id, top_k=top_k)
        search_time = time.time()
        
        total_time_ms = int((search_time - start_time) * 1000)
        embed_time_ms = int((embedding_time - start_time) * 1000)
        vec_time_ms = int((search_time - embedding_time) * 1000)
        
        return {
            "query": query,
            "results": results,
            "search_time_ms": total_time_ms,
            "timing_breakdown": {
                "embedding_ms": embed_time_ms,
                "vector_search_ms": vec_time_ms
            }
        }

# Singleton instance
_knowledge_repo = None

def get_knowledge_repository() -> KnowledgeRepository:
    global _knowledge_repo
    if _knowledge_repo is None:
        _knowledge_repo = KnowledgeRepository()
    return _knowledge_repo
