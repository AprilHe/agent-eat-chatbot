from openai import OpenAI
from config.config import Config

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def build_system_prompt(user_info):
    """Build system prompt with user information."""
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
    """Generate a response using the OpenAI API."""
    # Build system prompt with user information
    system_prompt = build_system_prompt(user_info)
    
    # Add system message at the beginning
    all_messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent conversation history (limit to avoid token limit)
    max_history = Config.MAX_HISTORY
    all_messages.extend(messages[-max_history:] if len(messages) > max_history else messages)
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=all_messages,
        temperature=Config.TEMPERATURE,
        max_tokens=Config.MAX_TOKENS
    )
    
    # Return response content
    return response.choices[0].message.content 