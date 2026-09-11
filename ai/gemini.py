import os
import json
import logging
from google import genai
from google.genai import types
from .base import AIProvider
from .schemas import MeetingInsightsSchema
from tenacity import retry, stop_after_attempt, wait_exponential

from .prompts.meeting_intelligence_prompt import MEETING_ANALYSIS_PROMPT, SYNTHESIS_PROMPT, QA_PROMPT

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        self.client = genai.Client(api_key=api_key)
        self.models_to_try = ['gemini-3.6-flash', 'gemini-3.5-flash']
        self.model_name = None
        self.max_chunk_length = 80000  # characters
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    def _call_gemini_with_retry(self, prompt: str, schema=None) -> str:
        last_error = None
        for model_name in self.models_to_try:
            try:
                config_kwargs = {}
                if schema:
                    config_kwargs["response_mime_type"] = "application/json"
                    config_kwargs["response_schema"] = schema
                
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None,
                )
                self.model_name = model_name
                return response.text
            except Exception as e:
                logger.warning(f"Failed with model {model_name}: {e}")
                last_error = e
        
        raise RuntimeError(f"All Gemini models failed: {last_error}")

    def _chunk_transcript(self, transcript: str) -> list[str]:
        chunks = []
        current_chunk = ""
        lines = transcript.split('\n')
        for line in lines:
            if len(current_chunk) + len(line) > self.max_chunk_length:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def generate_insights(self, transcript: str) -> dict:
        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty.")
            
        chunks = self._chunk_transcript(transcript)
        
        if len(chunks) == 1:
            return self._process_single_chunk(chunks[0])
        else:
            # Multi-chunk processing
            intermediate_results = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                try:
                    result = self._process_single_chunk(chunk)
                    intermediate_results.append(result)
                except Exception as e:
                    logger.error(f"Failed on chunk {i+1}: {e}")
                    
            # Combine intermediate results
            return self._synthesize_results(intermediate_results)

    def _process_single_chunk(self, chunk: str) -> dict:
        prompt = MEETING_ANALYSIS_PROMPT.format(transcript=chunk)
        raw_json = self._call_gemini_with_retry(prompt, MeetingInsightsSchema)
        try:
            parsed_json = json.loads(raw_json)
            validated_data = MeetingInsightsSchema(**parsed_json)
            return validated_data.model_dump()
        except Exception as e:
            logger.error(f"Validation failed for chunk: {e}")
            raise RuntimeError(f"Validation failed: {e}")

    def _synthesize_results(self, results: list[dict]) -> dict:
        synthesis_prompt = SYNTHESIS_PROMPT.format(results=json.dumps(results, indent=2))
        raw_json = self._call_gemini_with_retry(synthesis_prompt, MeetingInsightsSchema)
        try:
            parsed_json = json.loads(raw_json)
            validated_data = MeetingInsightsSchema(**parsed_json)
            return validated_data.model_dump()
        except Exception as e:
            logger.error(f"Validation failed for synthesis: {e}")
            raise RuntimeError(f"Validation failed: {e}")

    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        prompt = QA_PROMPT.format(transcript=transcript, question=question, insights=insights)
        return self._call_gemini_with_retry(prompt)
