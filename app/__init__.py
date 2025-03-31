from flask import Flask
import os
import logging
from .data_manager import DataManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    try:
        logger.debug("Starting application creation...")
        app = Flask(__name__)
        
        # Load configuration
        from .config import Config
        app.config.from_object(Config)
        
        # Initialize data
        with app.app_context():
            logger.debug("Initializing data storage...")
            from .models import init_data
            init_data()
            logger.debug("Data storage initialized")
        
        # Register blueprints
        from .routes import views
        app.register_blueprint(views)
        
        logger.debug("Application creation completed successfully")
        return app
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        raise

# Create the application instance
app = create_app() 