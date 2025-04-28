from crewai.tools import BaseTool, tool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

@tool("Synthetic Food Search")
def synthetic_food_search(query: str) -> list:
    """Returns a hardcoded list of food results for testing and synthetic integration."""
    return [
        {"name": "Kung Pao Chicken", "price": 15.99},
        {"name": "Mapo Tofu", "price": 12.50},
        {"name": "Sweet and Sour Pork", "price": 14.00},
        {"name": "Peking Duck", "price": 25.00},
        {"name": "Sichuan Spicy Noodles", "price": 11.75},
        {"name": "Egg Fried Rice", "price": 9.50},
        {"name": "Spring Rolls", "price": 7.00},
        {"name": "Hot and Sour Soup", "price": 8.25},
        {"name": "Beef Chow Fun", "price": 16.00},
        {"name": "Steamed Dumplings", "price": 10.00},
    ]
