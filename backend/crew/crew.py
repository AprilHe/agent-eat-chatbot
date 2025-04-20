from crewai import Agent, Crew, Task, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import yaml
from pathlib import Path
from mem0 import Memory

# Load environment variables
load_dotenv()

# Initialize memory for conversational context
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memory",
            "path": "./chroma_db",
        },
    },
}

memory = Memory.from_config(config)

class ChatCrew:
    """A wrapper for CrewAI conversational chatbot."""
    
    def __init__(self):
        """Initialize the ChatCrew with configurations."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Load agent and task configurations
        self.config_dir = Path(__file__).parent.parent / "config" / "crew"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create agent config file if it doesn't exist
        self.agents_config_path = self.config_dir / "agents.yaml"
        if not self.agents_config_path.exists():
            with open(self.agents_config_path, "w") as f:
                f.write("""assistant:
  role: >
    Food Recommendation Assistant
  goal: >
    To provide personalized food recommendations based on user preferences and requirements.
  backstory: >
    You are an advanced AI assistant specialized in food recommendations. You have extensive knowledge 
    about various cuisines, dietary preferences, and restaurants. Your purpose is to help users 
    find the perfect food options based on their preferences, allergies, and other requirements.
    You can offer specific restaurant recommendations, dish suggestions, and understand complex
    dietary needs. You're friendly, empathetic, and always focused on user satisfaction.
""")
        
        # Create task config file if it doesn't exist
        self.tasks_config_path = self.config_dir / "tasks.yaml"
        if not self.tasks_config_path.exists():
            with open(self.tasks_config_path, "w") as f:
                f.write("""assistant_task:
  description: >
    Respond to the user's message: {user_message}. Consider their food preferences and requirements.
    Use the provided conversation history for context: {context}.
  expected_output: >
    A personalized food recommendation response that addresses the user's query.
""")
    
    def _load_yaml_config(self, file_path):
        """Load YAML configuration from file."""
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading YAML from {file_path}: {str(e)}")
            return {}
    
    def generate_response(self, messages, user_info):
        """Generate a response using CrewAI."""
        try:
            # Extract the latest user message
            latest_user_message = ""
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    latest_user_message = msg.get('content', '')
                    break
            
            if not latest_user_message:
                return "I couldn't understand your message. Could you please try again?"
            
            # Get user ID for memory operations
            user_id = user_info.get('name', 'default_user')
            
            # Add user message to memory
            memory.add(f"User: {latest_user_message}", user_id=user_id)
            
            # Retrieve relevant context from memory
            relevant_info = memory.search(query=latest_user_message, limit=5, user_id=user_id)
            
            # Handle different result formats (string or dict with 'memory' key)
            context_items = []
            for item in relevant_info:
                if isinstance(item, dict) and "memory" in item:
                    context_items.append(item["memory"])
                elif isinstance(item, str):
                    context_items.append(item)
                else:
                    context_items.append(str(item))
            
            context = "\n".join(context_items)
            
            # Load configurations
            agents_config = self._load_yaml_config(self.agents_config_path)
            tasks_config = self._load_yaml_config(self.tasks_config_path)
            
            # Create the assistant agent
            assistant = Agent(
                role=agents_config.get('assistant', {}).get('role', 'Food Assistant'),
                goal=agents_config.get('assistant', {}).get('goal', 'Help users find good food options'),
                backstory=agents_config.get('assistant', {}).get('backstory', 'You are a helpful AI assistant specialized in food delivery.'),
                verbose=True,
                allow_delegation=False,
                llm=ChatOpenAI(
                    model=self.model,
                    temperature=0.7,
                    api_key=self.api_key
                )
            )
            
            # Format user information for task context
            user_info_str = ""
            if user_info:
                for key, value in user_info.items():
                    if value:
                        user_info_str += f"{key}: {value}\n"
            
            # Create the assistant task
            task_description = tasks_config.get('assistant_task', {}).get('description', 
                "Respond to the user's message: {user_message}. Consider their food preferences. Use the provided context: {context}")
            
            # Fill in placeholders in the task description
            task_description = task_description.format(
                user_message=latest_user_message,
                context=context
            )
            
            # Add user information to the task description if available
            if user_info_str:
                task_description += f"\n\nUSER INFORMATION:\n{user_info_str}"
            
            task = Task(
                description=task_description,
                expected_output=tasks_config.get('assistant_task', {}).get('expected_output', "A personalized food recommendation"),
                agent=assistant
            )
            
            # Create and run the crew
            crew = Crew(
                agents=[assistant],
                tasks=[task],
                verbose=0,
                process=Process.sequential,
                memory=True
            )
            
            # Run the crew and get the result
            result = crew.kickoff()
            
            # Add assistant response to memory
            memory.add(f"Assistant: {result}", user_id=user_id)
            
            return result
            
        except Exception as e:
            import traceback
            print(f"Error in generate_response: {str(e)}")
            traceback.print_exc()
            return f"I'm having trouble processing your request. Please try again later." 