#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from latest_ai_development.crew import UberEatsOrdering

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the UberEats Ordering Assistant
    """
    inputs = {
        'postal_code': 'SW1A 1AA',
        'street_address': '10 Downing Street, London',
        'taste_preferences': 'medium spicy, not too salty',
        'preferred_food_types': 'Indian, Italian, British',
        'disliked_food_types': 'Japanese, Korean',
        'allergies': 'nuts, shellfish',
        'budget': '£20-30',
        'delivery_time': '19:00',
        'current_time': datetime.now().strftime('%H:%M')
    }
    
    try:
        UberEatsOrdering().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the ordering assistant: {e}")

def train():
    """
    Train the ordering assistant system
    """
    inputs = {
        "postal_code": "SW1A 1AA",
        "street_address": "10 Downing Street, London",
        "taste_preferences": "medium spicy, not too salty",
        "preferred_food_types": "Indian, Italian, British",
        "disliked_food_types": "Japanese, Korean",
        "allergies": "nuts, shellfish",
        "budget": "£20-30",
        "delivery_time": "19:00"
    }
    try:
        UberEatsOrdering().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred during training: {e}")

def replay():
    """
    Replay the processing of a specific order
    """
    try:
        UberEatsOrdering().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred during replay: {e}")

def test():
    """
    Test the ordering assistant system
    """
    inputs = {
        "postal_code": "SW1A 1AA",
        "street_address": "10 Downing Street, London",
        "taste_preferences": "medium spicy, not too salty",
        "preferred_food_types": "Indian, Italian, British",
        "disliked_food_types": "Japanese, Korean",
        "allergies": "nuts, shellfish",
        "budget": "£20-30",
        "delivery_time": "19:00",
        "current_time": datetime.now().strftime('%H:%M')
    }
    try:
        UberEatsOrdering().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred during testing: {e}")
