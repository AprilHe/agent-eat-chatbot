# AgentEats - Your AI Food Delivery Assistant

AgentEats is a cross-platform AI food delivery assistant that integrates Uber Eats, Deliveroo, DoorDash and other delivery services to help users find the best deals, recommend meals based on preferences, and manage the entire ordering process from placement to delivery tracking.

## System Overview

AgentEats serves as more than just a recommendation system—it's a trustworthy food companion that:

- Remembers your food preferences and habits
- Saves you money by comparing options across platforms
- Makes ordering effortless
- Helps with decision-making when you're undecided
- Provides a "set it and forget it" experience

### Target Users

- Busy professionals with limited lunch breaks
- Students on tight budgets
- Frequent food delivery users tired of comparing multiple apps
- Discount-focused consumers who want to find the best deals

## Project Structure

This project follows a clean, modular architecture:

```
agent-eat-chatbot/
├── backend/              # Backend server and AI logic
│   ├── config/           # Configuration files (agents, tasks)
│   └── src/              # Backend source code
├── frontend/             # Web interface
│   └── src/              # Frontend source code
├── shared/               # Shared utilities and types
├── data/                 # Persistent data storage
│   └── chroma_db/        # Vector database for memory
├── run.py                # Main entry point
└── pyproject.toml        # Project dependencies and configuration
```

## Features

- 🤖 **AgentEats Assistant**: AI-powered food delivery companion
- 💾 **Preference Learning**: Remembers your food preferences and ordering habits
- 💰 **Cross-Platform Comparison**: Compares prices, delivery times, and promotions across services
- 🛒 **Automated Ordering**: Streamlines the ordering process
- 📱 **Order Tracking**: Monitors delivery status and estimated arrival times
- 🌐 **Modern UI**: Web interface with chat history and responsive design
- 📊 **Personalized Recommendations**: Suggests options based on preferences and context

## Setup and Installation

### Prerequisites

- Python 3.12+
- OpenAI API key

### Quick Setup

Install and set up the entire project with one command:

```bash
uv venv -p 3.12 && source .venv/bin/activate && uv pip install -e . && cp .env.example .env
```

Edit the `.env` file to add your API keys.

### Step-by-Step Installation

1. Install uv (modern Python package manager):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate a virtual environment with Python 3.12:

```bash
uv venv -p 3.12
source .venv/bin/activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys including OPENAI_API_KEY
```

## Running the Application

### Web Interface

```bash
python run.py
```

Open your browser to http://localhost:8000

### CLI Version

```bash
python backend/run.py
```

## System Functionality

When interacting with AgentEats, the system will:

1. **Collect User Information**

   - Location/address for delivery
   - Food preferences (cuisines, flavors, restrictions, allergies)
   - Budget constraints
   - Delivery time requirements
   - Number of people eating

2. **Search & Compare Platforms**

   - Check UberEats, Deliveroo, DoorDash and other platforms
   - Compare prices, delivery fees, estimated delivery times
   - Find applicable discounts and promotions

3. **Generate Personalized Recommendations**

   - Provide 1-3 options with clear reasoning
   - Highlight savings opportunities and fast delivery options
   - Consider user's previous preferences and feedback

4. **Manage Orders**
   - Assist with order placement
   - Track delivery status
   - Help with any delivery issues

## Development

To install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run code quality tools:

```bash
ruff check .
black .
```

## Testing the System

Test the chatbot's functionality with these sample prompts:

```
"I'm hungry and want something for lunch"
"I need dinner delivered for two people tonight"
"I'm craving Thai food but don't want to spend more than $20"
"What's the fastest option for pizza delivery right now?"
```

## License

MIT
