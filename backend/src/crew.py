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


@tool("FoodSearch")
def food_search(postal_code: str, keywords: str) -> list:
    """Search for food given a postal code and keywords, returning real deliveroo results.
    """
    results = []
    error = None

    def run_in_thread():
        nonlocal results, error
        try:
            # Create and manage a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(scrape_ubereats(postal_code, keywords))
            loop.close()
        except Exception as e:
            print(f"Error in scraper thread: {e}")
            error = e

    # Create and start the thread
    thread = threading.Thread(target=run_in_thread)
    thread.start()
    thread.join() # Wait for the thread to complete

    if error:
        # Return an error indication if the thread failed
        return [{ "error": f"Failed to get results due to an error in the scraper: {error}" }]
    else:
        return results


@CrewBase
class ChatbotCrew:
    """Agent Eat Chatbot crew"""

    # Use relative paths for config files
    agents_config = os.path.join(Path(__file__).parent.parent, "src/config/agents.yaml")
    tasks_config = os.path.join(Path(__file__).parent.parent, "src/config/tasks.yaml")

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["assistant"],
            verbose=True,
            tools=[food_search],
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
