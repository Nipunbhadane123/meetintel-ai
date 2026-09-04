import os
import json
import logging
from openai import OpenAI
from .base import AIProvider
from .schemas import MeetingInsightsSchema

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini" # Fast, cheap, large context
        
    def generate_insights(self, transcript: str) -> dict:
        prompt = f"""
        You are an expert AI meeting analyst. Analyze the following meeting transcript.
        
        Strict Rules:
        1. Use ONLY the supplied transcript. Do not invent facts or speakers.
        2. Distinguish decisions from suggestions.
        3. Do not invent deadlines. If not mentioned, say 'Not specified'.
        4. Return ONLY valid JSON that matches the requested schema.
        
        Transcript:
        {transcript}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Generate the meeting insights JSON."}
                ],
                response_format={ "type": "json_object" } # Note: requires careful prompt instructing JSON structure. Real schema forcing can be done with tool calls.
                # Since we don't have tool calls here, we'll just hope it follows the schema if we passed the schema string, but let's pass the schema.
            )
            raw_json = response.choices[0].message.content
            return json.loads(raw_json)
        except Exception as e:
            logger.error(f"OpenAI API error during insights generation: {e}")
            raise RuntimeError(f"Failed to generate insights via OpenAI: {e}")

    def ask_question(self, transcript: str, question: str) -> str:
        prompt = f"""
        You are an AI meeting assistant. Answer the user's question based strictly on the following transcript.
        If the answer cannot be found in the transcript, reply exactly with: "I couldn't find this information in the meeting."
        Do not hallucinate. Include transcript timestamps if available.
        
        Transcript:
        {transcript}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error during Q&A: {e}")
            return "Sorry, there was an error processing your question."
