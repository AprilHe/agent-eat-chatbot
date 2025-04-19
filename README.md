# Agent-Eat Chatbot

A chatbot that helps users find and order food from restaurants.

## Installation

Step-by-step instructions on how to install and set up the project locally.

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
   cp .env_template .env
   ```
   Edit the `.env` file with your API keys and configuration.

4. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. Use a simple HTTP server to provide frontend files
   - In a new terminal window, navigate to the directory containing chatbot.html, then run:
     ```bash
     python -m http.server 8000
     ```
   - Access the chatbot at http://localhost:8000/chatbot.html
2. Start a conversation with the chatbot.
3. Use the mode toggle to switch between guided and free conversation modes.

## Contributing

Contributions are welcome! Please read our [contribution guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
