import os
import logging
from .provider_manager import AIProviderManager

logger = logging.getLogger(__name__)

def get_ai_provider():
    return AIProviderManager()

class MeetingAnalyzer:
    def __init__(self):
        self.provider = get_ai_provider()
        
    def analyze(self, transcript_text: str) -> dict:
        """Generates all meeting insights from transcript."""
        logger.info("Starting AI meeting analysis...")
        import time
        start = time.time()
        res = self.provider.generate_insights(transcript_text)
        logger.info(f"AI meeting analysis completed in {time.time() - start:.2f}s")
        return res
        
    def ask(self, transcript_text: str, question: str, insights: str = "") -> str:
        """Ask a specific question about the meeting."""
        import time
        start = time.time()
        res = self.provider.ask_question(transcript_text, question, insights)
        logger.info(f"Ask AI completed in {time.time() - start:.2f}s")
        return res

    def rag_ask(self, question: str, user_id: str = None, meeting_id: str = None, org_id: str = None) -> dict:
        """Ask a question using RAG over the knowledge repository with tenant boundary."""
        from ai.rag import RAGService
        service = RAGService()
        return service.ask(question, user_id=user_id, meeting_id=meeting_id, org_id=org_id)
