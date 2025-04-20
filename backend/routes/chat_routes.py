from flask import Blueprint, request, jsonify
from utils.chat_utils import generate_chat_response
from utils.memory_utils import add_to_memory, get_relevant_context
import traceback

# Create a blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        # Get message history and user information from request
        data = request.json
        print(f"Request data: {data}")
        messages = data.get('messages', [])
        user_info = data.get('user_info', {})
        
        print(f"Messages: {messages}")
        print(f"User info: {user_info}")
        
        # Get the latest user message for memory search safely
        latest_message = ""
        if messages and isinstance(messages, list) and len(messages) > 0:
            last_msg = messages[-1]
            if isinstance(last_msg, dict) and last_msg.get('role') == 'user':
                latest_message = last_msg.get('content', '')
        
        print(f"Latest message: {latest_message}")
        
        # Ensure we have a user_id for memory operations
        user_id = user_info.get('name', 'default_user')
        print(f"User ID: {user_id}")
        
        # Generate response using CrewAI
        response = generate_chat_response(messages, user_info)
        
        # Convert CrewOutput to string if necessary
        if hasattr(response, 'raw_output'):
            response_text = response.raw_output
        elif hasattr(response, '__str__'):
            response_text = str(response)
        else:
            response_text = "I received your message but couldn't generate a proper response."
        
        # Store messages in memory
        if latest_message:
            add_to_memory(latest_message, "User", user_id=user_id)
        add_to_memory(response_text, "Assistant", user_id=user_id)
        
        return jsonify({'response': response_text})
        
    except Exception as e:
        # Error handling
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Error processing request', 'details': str(e)}), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200 