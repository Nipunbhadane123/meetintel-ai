import os
import json
import logging
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APITimeoutError, InternalServerError
from .base import AIProvider, AIProviderError, TransientAIError, QuotaExhaustedError, AuthError
from .schemas import MeetingInsightsSchema
from .prompts.meeting_intelligence_prompt import MEETING_ANALYSIS_PROMPT, SYNTHESIS_PROMPT, QA_PROMPT

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AuthError("OPENAI_API_KEY not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
    @property
    def provider_name(self) -> str:
        return "openai"
        
    def _handle_openai_error(self, e: Exception):
        logger.warning(f"OpenAI error: {e}")
        if isinstance(e, AuthenticationError):
            raise AuthError(f"OpenAI Auth Error: {e}")
        elif isinstance(e, RateLimitError):
            err_str = str(e).lower()
            if "quota" in err_str or "exceeded" in err_str:
                raise QuotaExhaustedError(f"OpenAI Quota Exhausted: {e}")
            else:
                raise TransientAIError(f"OpenAI Rate Limit: {e}")
        elif isinstance(e, (APIConnectionError, APITimeoutError, InternalServerError)):
            raise TransientAIError(f"OpenAI Transient Error: {e}")
        else:
            raise AIProviderError(f"OpenAI Error: {e}")

    def generate_insights(self, transcript: str) -> dict:
        prompt = MEETING_ANALYSIS_PROMPT.format(transcript=transcript)
        
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI meeting analyst."},
                    {"role": "user", "content": prompt}
                ],
                response_format=MeetingInsightsSchema,
            )
            return response.choices[0].message.parsed.model_dump()
        except Exception as e:
            self._handle_openai_error(e)
            
    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        prompt = QA_PROMPT.format(transcript=transcript, question=question, insights=insights)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful meeting assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            self._handle_openai_error(e)

    def rag_ask_question(self, context: str, question: str) -> dict:
        from .prompts.meeting_intelligence_prompt import RAG_QA_PROMPT
        from ai.rag import RAGResponse
        prompt = RAG_QA_PROMPT.format(context=context, question=question)
        
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful knowledge assistant."},
                    {"role": "user", "content": prompt}
                ],
                response_format=RAGResponse,
            )
            return response.choices[0].message.parsed.model_dump()
        except Exception as e:
            self._handle_openai_error(e)
