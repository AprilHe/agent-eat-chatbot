from camel.toolkits import (
    BrowserToolkit,
)
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
import os
import logging
import atexit
import signal
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Create model configuration for GPT-4o-mini
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O_MINI,
)

def cleanup():
    """Cleanup function to ensure browser is properly closed"""
    try:
        if 'browser_toolkit' in globals():
            browser_toolkit.browser.close()
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")

# Register cleanup function
atexit.register(cleanup)

def signal_handler(signum, frame):
    """Handle termination signals"""
    logger.info("Received termination signal, cleaning up...")
    cleanup()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Initialize browser toolkit with debugging options
    browser_toolkit = BrowserToolkit(
        history_window=50,
        web_agent_model=model,
        planning_agent_model=model,
        headless=True,  # Set to True if you don't want to see the browser
        channel="chromium",  # Explicitly specify chromium
        cache_dir=os.path.join(os.getcwd(), "browser_cache")  # Use a specific cache directory
    )
    
    # Run the browser automation
    browser_toolkit.browse_url(
        task_prompt="""
You MUST use browser toolkit to finish the task, you have been given one tool to open a web browser directly, go to Uber Eats.
Enter the delivery address: EC1R 0EH 22 Haywards PL.
Search for Chinese food.
From the search results, identify the top 10 restaurants.

For each of these restaurants:

Browse the entire restaurant page.

Look for the dish Kung Pao Chicken.

If found, add it to the cart and proceed to checkout.

On the order page:

Collect the price information.

Among all dishes priced between £12 and £20, find the one with the highest rating.

Place the order for that item using a gift card as the payment method.

NEVER close the browser until all tasks done
""",
        start_url="https://www.ubereats.com/"
    )
except Exception as e:
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
    cleanup()  # Ensure cleanup happens even on error
    raise