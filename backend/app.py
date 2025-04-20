from flask import Flask
from flask_cors import CORS
from config.config import Config
from routes.chat_routes import chat_bp
from routes.static_routes import static_bp

def create_app():
    """Initialize and configure the Flask application."""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(static_bp)
    
    return app

# Create the Flask application
app = create_app()

# Main program entry
if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=Config.PORT, 
        debug=Config.DEBUG
    )