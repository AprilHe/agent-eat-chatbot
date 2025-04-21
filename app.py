#!/usr/bin/env python
import os
import threading
import subprocess
import webbrowser
import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Agent Eat Chatbot</title>
        <meta http-equiv="refresh" content="0;url=http://localhost:8000">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        </style>
    </head>
    <body>
        <h1>Redirecting to Agent Eat Chatbot UI...</h1>
        <p>If you are not redirected automatically, <a href="http://localhost:8000">click here</a>.</p>
    </body>
    </html>
    """

def run_chatbot_backend():
    subprocess.run(["python", "backend/run.py"])

def run_chat_ui():
    subprocess.run(["python", "run.py"])

def open_browser():
    time.sleep(2)  # Wait for servers to start
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    print("Starting Agent Eat Chatbot...")
    
    # Start the backend in a separate thread
    backend_thread = threading.Thread(target=run_chatbot_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start the UI in a separate thread
    ui_thread = threading.Thread(target=run_chat_ui)
    ui_thread.daemon = True
    ui_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the main Flask app
    app.run(host='0.0.0.0', port=3000) 