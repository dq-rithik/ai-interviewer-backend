import os
from dotenv import load_dotenv

# Load environment variables from .env file (override=True ensures .env always wins)
load_dotenv(override=True)

class Config:
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    # AI Provider Selection
    # Default is 'groq'. If not specified, we can auto-detect based on available keys.
    DEFAULT_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    
    # Model Configurations
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

    @classmethod
    def get_active_provider(cls):
        """
        Returns the active AI provider based on environment config.
        If the selected provider lacks an API key, it falls back to any provider that has a key.
        """
        provider = cls.DEFAULT_PROVIDER
        
        # Verify key exists for the chosen provider, otherwise find a fallback
        if provider == "groq" and cls.GROQ_API_KEY:
            return "groq"
        elif provider == "gemini" and cls.GEMINI_API_KEY:
            return "gemini"
        elif provider == "openai" and cls.OPENAI_API_KEY:
            return "openai"
        elif provider == "claude" and cls.CLAUDE_API_KEY:
            return "claude"
            
        # Fallbacks if default is not available
        if cls.GROQ_API_KEY:
            return "groq"
        if cls.GEMINI_API_KEY:
            return "gemini"
        if cls.OPENAI_API_KEY:
            return "openai"
        if cls.CLAUDE_API_KEY:
            return "claude"
            
        # If no keys are configured, return the default anyway (it will error gracefully on API call)
        return provider
