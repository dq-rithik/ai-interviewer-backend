import logging
from app.services.ai import get_ai_provider
from app.config import Config

logger = logging.getLogger(__name__)

def generate_interview_questions(profile: dict, config: dict) -> list:
    """
    Generates interview questions using the active AI provider.
    """
    active_provider_name = Config.get_active_provider()
    logger.info(f"Using AI provider '{active_provider_name}' for question generation.")
    
    try:
        provider = get_ai_provider(active_provider_name)
        questions = provider.generate_questions(profile, config)
        
        # Post-process questions to ensure they have IDs
        for idx, q in enumerate(questions, 1):
            q["id"] = q.get("id", idx)
            
        return questions
    except Exception as e:
        logger.error(f"Error in question generation service: {str(e)}")
        raise e
