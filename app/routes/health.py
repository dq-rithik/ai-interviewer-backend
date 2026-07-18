from flask import Blueprint, jsonify
from app.config import Config

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    active_provider = Config.get_active_provider()
    
    return jsonify({
        "status": "healthy",
        "active_provider": active_provider,
        "configured_providers": {
            "groq": bool(Config.GROQ_API_KEY),
            "gemini": bool(Config.GEMINI_API_KEY),
            "openai": bool(Config.OPENAI_API_KEY),
            "claude": bool(Config.CLAUDE_API_KEY)
        }
    }), 200
