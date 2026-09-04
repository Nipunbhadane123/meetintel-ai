from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate_insights(self, transcript: str) -> dict:
        """Analyze the transcript and return structured JSON conforming to MeetingInsightsSchema."""
        pass
        
    @abstractmethod
    def ask_question(self, transcript: str, question: str) -> str:
        """Answer a question based strictly on the transcript."""
        pass
