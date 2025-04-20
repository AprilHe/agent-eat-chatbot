from mem0 import Memory
import os
import traceback

# Configuration for memory store
MEMORY_CONFIG = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "food_chatbot_memory",
            "path": "./chroma_db",
        },
    },
}

# Initialize memory
try:
    memory = Memory.from_config(MEMORY_CONFIG)
except Exception as e:
    print(f"Error initializing memory: {str(e)}")
    traceback.print_exc()
    memory = None

def add_to_memory(message, role, user_id="default_user"):
    """Add a message to memory."""
    try:
        if memory:
            memory.add(f"{role}: {message}", user_id=user_id)
    except Exception as e:
        print(f"Error adding to memory: {str(e)}")
        traceback.print_exc()

def search_memory(query, limit=3, user_id="default_user"):
    """Search memory for relevant information."""
    try:
        if memory:
            results = memory.search(query=query, limit=limit, user_id=user_id)
            
            # Debug the results before processing
            print(f"Memory search results for '{query[:20]}...': {results}")
            
            # Handle different result formats
            memories = []
            for result in results:
                if isinstance(result, dict) and "memory" in result:
                    memories.append(result["memory"])
                elif isinstance(result, str):
                    memories.append(result)
                else:
                    # Convert any other type to string
                    memories.append(str(result))
            
            return memories
        return []
    except Exception as e:
        print(f"Error searching memory: {str(e)}")
        traceback.print_exc()
        return []

def get_relevant_context(query, user_id="default_user"):
    """Get relevant context from memory as a string."""
    try:
        memories = search_memory(query, user_id=user_id)
        return "\n".join(memories) if memories else ""
    except Exception as e:
        print(f"Error getting relevant context: {str(e)}")
        traceback.print_exc()
        return "" 