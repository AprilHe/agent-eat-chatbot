import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
class Config:
    # Flask settings
    PORT = int(os.getenv("PORT", 5001))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o"
    
    # Chat settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    MAX_HISTORY = 10  # Maximum number of messages to keep in history
    
    # System prompt
    BASE_SYSTEM_PROMPT = """You are a friendly AI assistant responsible for collecting user information and answering questions. 
Your main task is to understand users' dining preferences and requirements to provide personalized food recommendations.""" 