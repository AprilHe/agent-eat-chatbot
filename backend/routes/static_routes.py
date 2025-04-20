from flask import Blueprint, send_from_directory

# Create a blueprint for static routes
static_bp = Blueprint('static', __name__)

@static_bp.route('/')
def index():
    """Serve the main page."""
    return send_from_directory('../frontend', 'index.html')

@static_bp.route('/chatbot.html')
def chatbot():
    """Legacy route for the chatbot interface."""
    return send_from_directory('../frontend', 'index.html')

@static_bp.route('/css/<path:path>')
def serve_css(path):
    """Serve CSS files."""
    return send_from_directory('../frontend/css', path)

@static_bp.route('/js/<path:path>')
def serve_js(path):
    """Serve JavaScript files."""
    return send_from_directory('../frontend/js', path) 