from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate_insights(self, transcript: str) -> dict:
        pass
        
    @abstractmethod
    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        pass
