from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import sys
from pathlib import Path
from crewai.tools import tool
import asyncio
import threading
from .uber_eats_scraper import scrape_ubereats

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))


# @tool("FoodSearch")
# def food_search(postal_code: str, keywords: str) -> list:
#     """Search for food given a postal code and keywords, returning real deliveroo results.
#     """
#     results = []
#     error = None
#
#     def run_in_thread():
#         nonlocal results, error
#         try:
#             # Create and manage a new event loop for this thread
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             results = loop.run_until_complete(scrape_ubereats(postal_code, keywords))
#             loop.close()
#         except Exception as e:
#             print(f"Error in scraper thread: {e}")
#             error = e
#
#     # Create and start the thread
#     thread = threading.Thread(target=run_in_thread)
#     thread.start()
#     thread.join() # Wait for the thread to complete
#
#     if error:
#         # Return an error indication if the thread failed
#         return [{ "error": f"Failed to get results due to an error in the scraper: {error}" }]
#     else:
#         return results

@tool("FoodSearch")
def food_search(postal_code: str, keywords: str) -> list:
    """
    Search for food given a postal code and keywords. Returns a result based on the keywords provided.
    
    Supported keywords and their results:
    - "pizza": Returns a Margherita Pizza from Pizza Place.
    - "sushi": Returns a Salmon Sushi Set from Sushi Bar.
    - "burger": Returns a Classic Burger from Burger Joint.
    
    If the keywords do not match any of the above, an error message is returned.
    """
    # This dictionary will be injected into the agent below
    keyword_map = {
        "pizza": [{"name": "Margherita Pizza", "price": 10.99, "restaurant": "Pizza Place", "rating": 4.5}],
        "sushi": [{"name": "Salmon Sushi Set", "price": 15.99, "restaurant": "Sushi Bar", "rating": 4.7}],
        "burger": [{"name": "Classic Burger", "price": 9.99, "restaurant": "Burger Joint", "rating": 4.3}],
    }
    for key, value in keyword_map.items():
        if key in keywords.lower():
            return value
    return [{"error": "No matching food found for the given keywords."}]


@tool("PayOrder")
def pay_order(order_id: str, payment_method: str) -> dict:
    """Pay for an order given an order ID and payment method."""
    if not order_id or not payment_method:
        return {"error": "Missing order_id or payment_method"}
    return {
        "order_id": order_id,
        "status": "paid",
        "payment_method": payment_method,
        "message": f"Order {order_id} has been paid using {payment_method}."
    }


@CrewBase
class ChatbotCrew:
    """Agent Eat Chatbot crew"""

    # Use relative paths for config files
    agents_config = os.path.join(Path(__file__).parent.parent, "src/config/agents.yaml")
    tasks_config = os.path.join(Path(__file__).parent.parent, "src/config/tasks.yaml")

    @agent
    def assistant(self) -> Agent:
        # Hardcoded keyword-to-result mapping for demo
        self.keyword_map = {
            "pizza": [{"name": "Margherita Pizza", "price": 10.99, "restaurant": "Pizza Place", "rating": 4.5}],
            "sushi": [{"name": "Salmon Sushi Set", "price": 15.99, "restaurant": "Sushi Bar", "rating": 4.7}],
            "burger": [{"name": "Classic Burger", "price": 9.99, "restaurant": "Burger Joint", "rating": 4.3}],
        }
        return Agent(
            config=self.agents_config["assistant"],
            verbose=True,
            tools=[food_search, pay_order],
        )

    @task
    def assistant_task(self) -> Task:
        return Task(config=self.tasks_config["assistant_task"], agent=self.assistant())

    @crew
    def crew(self) -> Crew:
        """Creates the chatbot crew"""

        print("Registered tools:", self.assistant().tools)

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
