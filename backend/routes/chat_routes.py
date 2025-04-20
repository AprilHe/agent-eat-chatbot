from flask import Blueprint, request, jsonify
from utils.chat_utils import generate_chat_response

# Create a blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        # Get message history and user information from request
        data = request.json
        messages = data.get('messages', [])
        user_info = data.get('user_info', {})
        
        # Generate response using OpenAI
        reply = generate_chat_response(messages, user_info)
        
        return jsonify({'response': reply})
        
    except Exception as e:
        # Error handling
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error processing request', 'details': str(e)}), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200 