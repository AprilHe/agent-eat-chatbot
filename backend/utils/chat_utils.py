from crew.crew import ChatCrew
from config.config import Config
import traceback
import sys

# Initialize chat crew
chat_crew = ChatCrew()

def build_system_prompt(user_info):
    """Build system prompt with user information (kept for compatibility)."""
    system_prompt = Config.BASE_SYSTEM_PROMPT
    
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
    
    return system_prompt

def generate_chat_response(messages, user_info):
    """Generate a response using CrewAI instead of direct OpenAI API calls."""
    try:
        print("-" * 40)
        print("In generate_chat_response")
        print(f"Messages: {messages}")
        print(f"User info: {user_info}")
        print(f"OpenAI API Key: {Config.OPENAI_API_KEY[:5]}...")
        
        # Sanity check for data types
        if not isinstance(messages, list):
            print(f"ERROR: messages is not a list: {type(messages)}")
            return "I'm sorry, there was an issue with the message format."
            
        if not isinstance(user_info, dict):
            print(f"ERROR: user_info is not a dict: {type(user_info)}")
            return "I'm sorry, there was an issue with the user information format."
        
        # Limit messages to avoid token limit
        max_history = Config.MAX_HISTORY
        limited_messages = messages[-max_history:] if len(messages) > max_history else messages
        
        print(f"Limited messages: {limited_messages}")
        
        # Generate response using the crew
        response = chat_crew.generate_response(limited_messages, user_info)
        
        print(f"Response: {response}")
        print("-" * 40)
        
        # Return response content
        return response
    except Exception as e:
        print(f"ERROR in generate_chat_response: {str(e)}")
        print(f"Exception type: {type(e)}")
        traceback.print_exc(file=sys.stdout)
        # Return a fallback response
        return "I'm having trouble connecting to my language model. Please try again later." 