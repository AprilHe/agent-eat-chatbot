from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

@CrewBase
class ChatbotCrew:
    """Agent Eat Chatbot crew"""

    # Use relative paths for config files
    agents_config = os.path.join(Path(__file__).parent.parent, "config/agents.yaml")
    tasks_config = os.path.join(Path(__file__).parent.parent, "config/tasks.yaml")

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["assistant"],
            verbose=True,
        )

    @task
    def assistant_task(self) -> Task:
        return Task(config=self.tasks_config["assistant_task"], agent=self.assistant())

    @crew
    def crew(self) -> Crew:
        """Creates the chatbot crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=0,
        )
