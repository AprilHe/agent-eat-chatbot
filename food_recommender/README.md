# Travel Assistant Crew

A CrewAI-powered virtual travel planning assistant that helps you research destinations, plan itineraries, and discover authentic local experiences.

## Features

- **Destination Research**: Get comprehensive information about any travel destination
- **Itinerary Planning**: Receive a detailed day-by-day itinerary for your trip
- **Local Insights**: Discover hidden gems and authentic experiences from a virtual local expert

## Agents

1. **Travel Researcher**: Researches destinations, attractions, and travel information
2. **Itinerary Planner**: Creates optimized day-by-day travel schedules
3. **Local Expert**: Provides insider knowledge and authentic local experiences

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API keys in the environment:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export SERPER_API_KEY=your_serper_api_key  # Optional for web search
   ```

## Using with CrewAI Chat UI

To interact with this crew using the CrewAI Chat UI:

1. Navigate to the travel_assistant_crew directory:

   ```bash
   cd travel_assistant_crew
   ```

2. Start the CrewAI Chat UI:

   ```bash
   crewai-chat-ui
   ```

3. Open your browser and go to the provided URL (usually http://localhost:8000)

4. Start chatting with your travel planning crew!

## Example Questions

- "I'm planning a trip to Japan for 7 days. Can you help me plan it?"
- "What are the must-see attractions in Paris?"
- "I want to experience authentic local cuisine in Thailand. What do you recommend?"
- "What's the best time to visit New Zealand?"

## Notes

- The more specific you are about your travel preferences, the better the recommendations will be
- You can specify details like your budget, travel style, interests, and any specific requirements
- The crew works sequentially, with each agent building on the work of the previous agent
