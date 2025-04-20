# Agent-Eat Chatbot

A chatbot that helps users find and order food from restaurants based on their preferences.

## Project Structure

The project has been organized into a modular structure:

```
agent-eat-chatbot/
├── frontend/              # Frontend code
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── templates/         # HTML templates
│   ├── index.html         # Main application
│   └── chatbot.html       # Redirect to index.html
├── backend/               # Backend code
│   ├── config/            # Configuration files
│   ├── routes/            # API routes
│   ├── utils/             # Utility functions
│   ├── .env               # Environment variables
│   └── app.py             # Main application
└── requirements.txt       # Python dependencies
```

## Installation

Step-by-step instructions on how to install and set up the project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/AprilHe/agent-chat-chatbot.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   cp backend/.env_template backend/.env
   ```

   Edit the `.env` file with your OpenAI API key and other configuration options.

4. Run the backend application:
   ```bash
   cd backend
   python app.py
   ```

## Usage

1. After starting the backend server, the application is accessible at:

   - Main interface: http://localhost:5001/
   - Legacy interface: http://localhost:5001/chatbot.html
   - Health check: http://localhost:5001/health

2. Start a conversation with the chatbot:

   - In guided mode, the chatbot will ask you questions about your food preferences
   - In free conversation mode, you can ask anything about food recommendations

3. Use the mode toggle to switch between guided and free conversation modes.

## Features

- **Guided Conversation Mode**: The chatbot asks specific questions to understand your preferences.
- **Free Conversation Mode**: Chat freely about food recommendations.
- **Preference Storage**: Your preferences are stored during the session and used to personalize recommendations.
- **Responsive Design**: Works well on both desktop and mobile devices.

## API Endpoints

- `GET /`: Serves the main chatbot interface
- `GET /health`: Health check endpoint
- `POST /api/chat`: Chat API endpoint that connects to OpenAI

## Contributing

Contributions are welcome! Please read our [contribution guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
