from app.services.ai.groq_provider import GroqProvider
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.claude_provider import ClaudeProvider

def get_ai_provider(provider_name: str):
    """
    Factory to retrieve an instance of the configured AI provider.
    """
    provider_name = provider_name.lower().strip()
    
    if provider_name == "groq":
        return GroqProvider()
    elif provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "claude":
        return ClaudeProvider()
    else:
        raise ValueError(f"Unknown AI Provider: {provider_name}. Supported providers are 'groq', 'gemini', 'openai', and 'claude'.")
