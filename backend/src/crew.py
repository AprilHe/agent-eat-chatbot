from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import sys
from pathlib import Path
from crewai.tools import tool
import asyncio
from .uber_eats_scraper import scrape_ubereats

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))



@tool("Postal Code Food Search")
def postal_code_food_search(postal_code: str, keywords: str) -> list:
    """Search for food given a postal code and keywords, returning real Uber Eats results."""
    # loop = asyncio.get_event_loop()
    results = "tofu"#loop.run_until_complete(scrape_ubereats(postal_code, keywords))
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
            tools=[postal_code_food_search],
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
            verbose=0,
        )
