import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool

# Initialize tools
website_tool = WebsiteSearchTool()

# Create specialized agents
food_recommender = Agent(
    role="Food Recommendation Specialist",
    goal="Recommend the best food options based on user preferences",
    backstory="""You are an expert in cuisines from around the world with 
    extensive knowledge of ingredients, flavor profiles, and dietary restrictions.
    You help people discover delicious food they'll love based on their 
    preferences, mood, and dietary needs.""",
    verbose=True,   
    tools=[website_tool]
)

menu_browser = Agent(
    role="Menu Browser and Researcher",
    goal="Find and browse restaurant menus to locate specific dishes",
    backstory="""You are an expert at finding restaurant menus online and
    browsing them efficiently to locate specific dishes, compare prices,
    and check availability. You're familiar with all major food delivery
    platforms and restaurant websites.""",
    verbose=True,
    tools=[website_tool]
)

order_processor = Agent(
    role="Order Processing Assistant",
    goal="Help users place their food orders accurately and efficiently",
    backstory="""You are an expert at handling food orders, making sure all
    details are correct, and ensuring a smooth ordering process. You confirm
    orders, handle special requests, and manage order tracking.""",
    verbose=True,
    tools=[website_tool]
)

# Define tasks
preference_task = Task(
    description="""Understand the user's food preferences and dietary restrictions.
    Ask clarifying questions about:
    - Cuisine preferences (Italian, Chinese, Mexican, etc.)
    - Dietary restrictions (vegetarian, vegan, gluten-free, etc.)
    - Spice level preferences
    - Any ingredients they want to avoid
    - Price range they're comfortable with
    - Occasion (casual meal, special occasion, etc.)
    
    Based on their answers, recommend 3-5 suitable food options with brief descriptions.
    """,
    agent=food_recommender,
    expected_output="A list of 3-5 personalized food recommendations with descriptions",
)

menu_search_task = Task(
    description="""Based on the user's selected food recommendation, search for
    restaurants or delivery options that offer this dish. For each option, provide:
    - Restaurant name
    - Price
    - Estimated delivery time (if applicable)
    - Rating (if available)
    - Any special offers or deals
    
    Allow the user to select their preferred restaurant/delivery option.
    """,
    agent=menu_browser,
    expected_output="A list of restaurant/delivery options for the selected food item",
    context=[preference_task],
)

order_task = Task(
    description="""Process the food order for the user's selected option. Help them:
    - Confirm the order details (items, quantities, special instructions)
    - Provide estimated delivery time or pickup information
    - Handle any payment-related questions (note: don't collect actual payment info)
    - Confirm the order and provide an order summary
    
    Ask if they need anything else before finalizing.
    """,
    agent=order_processor,
    expected_output="Order confirmation with summary and next steps",
    context=[preference_task, menu_search_task],
)

# Create the crew
food_ordering_crew = Crew(
    agents=[food_recommender, menu_browser, order_processor],
    tasks=[preference_task, menu_search_task, order_task],
    process=Process.sequential,
    verbose=True,
    memory=True
)

# This crew instance can be used with the CrewAI Chat UI
crew = food_ordering_crew 