from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv() 

# Initialize Flask application
app = Flask(__name__)
# Enable CORS
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Handle chat requests
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # 获取前端传来的消息历史和用户信息
        data = request.json
        messages = data.get("messages", [])
        user_info = data.get("user_info", {})
        
        # Build system prompt with user information
        system_prompt = "You are a friendly AI assistant responsible for collecting user information and answering questions. Your main task is to understand users' dining preferences and requirements to provide personalized food recommendations."
        
        # Add user information to system prompt
        if user_info:
            system_prompt += "\nUser Information:"
            if user_info.get('name'):
                system_prompt += f"\n- Name: {user_info.get('name')}"
            if user_info.get('address'):
                system_prompt += f"\n- Delivery Address: {user_info.get('address')}"
            if user_info.get('taste'):
                system_prompt += f"\n- Flavor Preferences: {user_info.get('taste')}"
            if user_info.get('favoriteFoods'):
                system_prompt += f"\n- Favorite Foods: {user_info.get('favoriteFoods')}"
            if user_info.get('dislikedFoods'):
                system_prompt += f"\n- Disliked Foods: {user_info.get('dislikedFoods')}"
            if user_info.get('allergies'):
                system_prompt += f"\n- Food Allergies: {user_info.get('allergies')}"
            if user_info.get('priceRange'):
                system_prompt += f"\n- Price Range: {user_info.get('priceRange')}"
            if user_info.get('deliveryTime'):
                system_prompt += f"\n- Delivery Time: {user_info.get('deliveryTime')}"
            system_prompt += f"\n- Number of Diners: {user_info.get('numberOfDiners', '1')}"
            
        # Add system message at the beginning of the message list
        all_messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history (limit message count to avoid exceeding token limit)
        max_history = 10  # Keep at most 10 recent messages
        all_messages.extend(messages[-max_history:] if len(messages) > max_history else messages)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # Or other model of your choice
            messages=all_messages,
            temperature=0.7,  # Balance between creativity and consistency
            max_tokens=1000  # Limit response length
        )
        
        # Get API response content
        reply = response.choices[0].message.content
        
        return jsonify({"response": reply})
        
    except Exception as e:
        # Error handling
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error processing request", "details": str(e)}), 500

# Add health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Main program entry
if __name__ == "__main__":
    # Get port, default to 5001 if not set in environment variables
    port = int(os.getenv("PORT", 5001))
    # Start application, enable debug mode in development environment
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")