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

class AIProviderError(Exception):
    pass

class TransientAIError(AIProviderError):
    pass

_model_health_cache = {}

class GeminiProvider(AIProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        self.client = genai.Client(api_key=api_key)
        
        primary = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-3.6-flash")
        fallbacks_str = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-3.5-flash-lite")
        fallbacks = [m.strip() for m in fallbacks_str.split(",") if m.strip()]
        
        self.models_to_try = [primary] + fallbacks
        self.model_name = None
        self.max_chunk_length = 80000  # characters
        
    def _call_gemini_with_retry(self, prompt: str, schema=None) -> str:
        import time
        import random
        last_error = None
        
        for model_name in self.models_to_try:
            # Check circuit breaker
            if model_name in _model_health_cache:
                expiry = _model_health_cache[model_name]
                if time.time() < expiry:
                    logger.info(f"Skipping {model_name} (circuit breaker active).")
                    continue
                else:
                    del _model_health_cache[model_name]
            
            for attempt in range(1, 4):  # 3 attempts per model
                try:
                    config_kwargs = {
                        "automatic_function_calling": {"disable": True}
                    }
                    if schema:
                        config_kwargs["response_mime_type"] = "application/json"
                        config_kwargs["response_schema"] = schema
                    
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(**config_kwargs),
                    )
                    self.model_name = model_name
                    return response.text
                except Exception as e:
                    logger.warning(f"Failed with model {model_name} (Attempt {attempt}): {e}")
                    err_str = str(e)
                    
                    is_quota = "quota" in err_str.lower() or ("429" in err_str and "exceeded" in err_str.lower())
                    is_404 = "404" in err_str
                    is_transient = any(code in err_str for code in ["500", "502", "503", "504", "timeout"]) or ("429" in err_str and not is_quota)
                    
                    if is_404 or is_quota:
                        logger.warning(f"Unrecoverable error (Quota/404) on {model_name}. Skipping to next model.")
                        # Circuit breaker: Mark unavailable for 5 minutes
                        _model_health_cache[model_name] = time.time() + 300
                        last_error = e
                        break
                        
                    if is_transient:
                        last_error = e
                        if attempt < 3:
                            import re
                            sleep_time = (2 ** (attempt - 1)) + random.uniform(0, 1)
                            match = re.search(r"'retryDelay':\s*'(\d+)s'", err_str)
                            if match:
                                delay = int(match.group(1))
                                if delay > 10:
                                    logger.warning(f"Retry delay too long ({delay}s), skipping {model_name}.")
                                    break
                                sleep_time = max(sleep_time, delay)
                            
                            logger.info(f"Retrying {model_name} in {sleep_time:.2f}s...")
                            time.sleep(sleep_time)
                        continue
                        
                    # Non-transient error (e.g. 400 Bad Request)
                    last_error = e
                    break
            
            # If we break or exhaust retries, continue to the next model
            
        if last_error:
            raise TransientAIError("MeetIntel AI is temporarily unable to reach the AI service.")
        raise RuntimeError("All Gemini models failed")

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

    def rag_ask_question(self, context: str, question: str) -> str:
        from .prompts.meeting_intelligence_prompt import RAG_QA_PROMPT
        prompt = RAG_QA_PROMPT.format(context=context, question=question)
        return self._call_gemini_with_retry(prompt)
