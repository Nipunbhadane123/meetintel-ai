import os
import json
import logging
import google.generativeai as genai
from .base import AIProvider
from .schemas import MeetingInsightsSchema

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        genai.configure(api_key=api_key)
        self.models_to_try = ['gemini-2.5-flash', 'gemini-3.5-flash', 'gemini-flash-latest']
        self.model = None
        
    def generate_insights(self, transcript: str) -> dict:
        prompt = f"""
        You are an expert AI meeting analyst. Analyze the following meeting transcript.
        
        Strict Rules:
        1. Use ONLY the supplied transcript. Do not invent facts or speakers.
        2. Distinguish decisions from suggestions.
        3. Do not invent deadlines. If not mentioned, say 'Not specified'.
        4. Return ONLY valid JSON that matches this exact schema:
        {MeetingInsightsSchema.model_json_schema()}
        
        Do not wrap the JSON in markdown code blocks. Just output raw JSON.
        
        Transcript:
        {transcript}
        """
        
        last_error = None
        for model_name in self.models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Try to generate content without response_mime_type to ensure compatibility with all models and SDKs
                response = model.generate_content(prompt)
                
                raw_json = response.text.strip()
                # Clean up markdown code blocks if the model ignored the instruction
                if raw_json.startswith("```json"):
                    raw_json = raw_json[7:]
                if raw_json.startswith("```"):
                    raw_json = raw_json[3:]
                if raw_json.endswith("```"):
                    raw_json = raw_json[:-3]
                    
                self.model = model # Cache the working model for Q&A
                return json.loads(raw_json.strip())
                
            except Exception as e:
                logger.warning(f"Failed with model {model_name}: {e}")
                last_error = e
                
        logger.error("All Gemini models failed.")
        raise RuntimeError(f"Failed to generate insights: {last_error}")

    def ask_question(self, transcript: str, question: str) -> str:
        if self.model is None:
            # Fallback for Q&A if insights weren't generated in this session
            for model_name in self.models_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    # Test if it works
                    break
                except Exception:
                    continue

        if self.model is None:
            self.model = genai.GenerativeModel('gemini-pro')
            
        prompt = f"""
        You are an AI meeting assistant. Answer the user's question based strictly on the following transcript.
        If the answer cannot be found in the transcript, reply exactly with: "I couldn't find this information in the meeting."
        Do not hallucinate. Include transcript timestamps if available.
        
        Transcript:
        {transcript}
        
        Question: {question}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error during Q&A: {e}")
            return "Sorry, there was an error processing your question."
