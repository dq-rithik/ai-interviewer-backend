import logging
from flask import Flask
from flask_cors import CORS
from app.config import Config

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configure app from Config class
    app.config.from_object(Config)
    
    # Enable CORS for all routes (specifically allows frontend port 5173 / localhost)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register Blueprints
    from app.routes.health import health_bp
    from app.routes.interview import interview_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(interview_bp, url_prefix='/api')
    
    logger.info("Flask application initialized successfully.")
    
    return app
