import os
import time
import logging
from .base import AIProvider, TransientAIError, QuotaExhaustedError, AuthError, AIProviderError
from .gemini import GeminiProvider
from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)

# Global cache for provider health
# structure: {"provider_name": {"status": "unhealthy", "expiry": timestamp}}
_provider_health = {}

class AIProviderManager:
    def __init__(self):
        self.cooldown_seconds = 120  # 2 minutes cooldown for failing providers
        
    def _instantiate_provider(self, provider_name: str) -> AIProvider:
        if provider_name == "gemini":
            return GeminiProvider()
        elif provider_name == "openai":
            return OpenAIProvider()
        raise ValueError(f"Unknown provider: {provider_name}")

    def _is_provider_healthy(self, provider_name: str) -> bool:
        if provider_name in _provider_health:
            health = _provider_health[provider_name]
            if health["status"] == "unhealthy" and time.time() < health["expiry"]:
                return False
            # Clear if expired
            if time.time() >= health["expiry"]:
                del _provider_health[provider_name]
        return True

    def _mark_provider_unhealthy(self, provider_name: str, duration_seconds: int = None):
        if not duration_seconds:
            duration_seconds = self.cooldown_seconds
        logger.warning(f"Marking provider '{provider_name}' as unhealthy for {duration_seconds}s.")
        _provider_health[provider_name] = {
            "status": "unhealthy",
            "expiry": time.time() + duration_seconds
        }

    def _get_provider_chain(self) -> list[str]:
        # Determine primary and fallback based on env config
        primary = os.getenv("AI_PRIMARY_PROVIDER", os.getenv("AI_PROVIDER", "gemini")).lower()
        if primary == "openai":
            return ["openai", "gemini"]
        return ["gemini", "openai"]

    def _execute_with_failover(self, method_name: str, *args, **kwargs):
        chain = self._get_provider_chain()
        last_error = None
        
        for provider_name in chain:
            if not self._is_provider_healthy(provider_name):
                logger.info(f"Skipping {provider_name} as it is currently marked unhealthy.")
                continue
                
            try:
                provider_instance = self._instantiate_provider(provider_name)
            except AuthError as e:
                logger.warning(f"{provider_name} is not configured correctly or auth failed: {e}")
                self._mark_provider_unhealthy(provider_name, 3600)  # long cooldown for auth issues
                last_error = e
                continue
            except Exception as e:
                logger.warning(f"Failed to instantiate {provider_name}: {e}")
                last_error = e
                continue

            try:
                logger.info(f"Attempting execution using {provider_name}...")
                method = getattr(provider_instance, method_name)
                result = method(*args, **kwargs)
                
                # Success! Record provider used
                import streamlit as st
                if hasattr(st, "session_state"):
                    st.session_state['last_ai_provider_used'] = provider_name
                
                return result
            except TransientAIError as e:
                logger.warning(f"{provider_name} encountered a transient error: {e}")
                # Wait exponential already handled mostly inside provider, 
                # but if it bubbled up, it means it failed after retries.
                self._mark_provider_unhealthy(provider_name)
                last_error = e
            except QuotaExhaustedError as e:
                logger.error(f"{provider_name} quota exhausted: {e}")
                self._mark_provider_unhealthy(provider_name, 3600) # long cooldown
                last_error = e
            except AuthError as e:
                logger.error(f"{provider_name} auth error: {e}")
                self._mark_provider_unhealthy(provider_name, 3600)
                last_error = e
            except Exception as e:
                logger.error(f"{provider_name} unexpected error: {e}")
                self._mark_provider_unhealthy(provider_name)
                last_error = e
                
        # If we get here, all providers failed
        if last_error:
            raise RuntimeError(f"All configured AI providers failed. Last error: {last_error}")
        raise RuntimeError("No configured AI providers are available.")

    def generate_insights(self, transcript: str) -> dict:
        return self._execute_with_failover("generate_insights", transcript)

    def ask_question(self, transcript: str, question: str, insights: str = "") -> str:
        return self._execute_with_failover("ask_question", transcript, question, insights)

    def rag_ask_question(self, context: str, question: str) -> str:
        # Fallback handling for rag_ask_question which may not exist directly on OpenAIProvider yet
        # Let's ensure OpenAIProvider implements it or fallback to base ask_question
        return self._execute_with_failover("rag_ask_question", context, question)

    @classmethod
    def get_provider_status(cls) -> dict:
        """Returns the health status of providers for the settings page."""
        status = {}
        for p in ["gemini", "openai"]:
            if os.getenv(f"{p.upper()}_API_KEY"):
                if p in _provider_health and _provider_health[p]["status"] == "unhealthy":
                    status[p] = "Temporarily Unavailable"
                else:
                    status[p] = "Available"
            else:
                status[p] = "Not Configured"
        return status
