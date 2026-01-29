from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Register blueprints/routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app