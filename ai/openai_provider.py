import os
import json
import logging
from openai import OpenAI
from .base import AIProvider
from .schemas import MeetingInsightsSchema
from .prompts.meeting_intelligence_prompt import MEETING_ANALYSIS_PROMPT, SYNTHESIS_PROMPT, QA_PROMPT

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
    def generate_insights(self, transcript: str) -> dict:
        prompt = MEETING_ANALYSIS_PROMPT.format(transcript=transcript)
        
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert AI meeting analyst."},
                {"role": "user", "content": prompt}
            ],
            response_format=MeetingInsightsSchema,
        )
        
        return response.choices[0].message.parsed.model_dump()
        
    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        prompt = QA_PROMPT.format(transcript=transcript, question=question, insights=insights)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful meeting assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
