from abc import ABC, abstractmethod

class AIProviderError(Exception):
    pass

class TransientAIError(AIProviderError):
    pass

class QuotaExhaustedError(AIProviderError):
    pass

class AuthError(AIProviderError):
    pass

class AIProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def generate_insights(self, transcript: str) -> dict:
        pass
        
    @abstractmethod
    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        pass
        
    @abstractmethod
    def rag_ask_question(self, context: str, question: str) -> dict:
        pass
