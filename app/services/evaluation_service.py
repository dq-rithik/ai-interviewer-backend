import logging
from app.services.ai import get_ai_provider
from app.config import Config

logger = logging.getLogger(__name__)

def evaluate_completed_interview(profile: dict, config: dict, questions: list, answers: dict) -> dict:
    """
    Evaluates the completed interview questions and candidate answers,
    using the active AI provider.
    """
    active_provider = Config.get_active_provider()
    logger.info(f"Using AI provider '{active_provider}' for interview evaluation.")
    
    try:
        provider = get_ai_provider(active_provider)
        report = provider.evaluate_interview(profile, config, questions, answers)
        return report
    except Exception as e:
        logger.error(f"Error in interview evaluation service: {str(e)}")
        raise e
