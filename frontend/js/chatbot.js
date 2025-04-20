// Chat flow configuration
const chatFlow = {
    currentStep: 0,
    questions: [
        {
            text: "Hello! I'm your AI assistant. Nice to meet you! What's your name?",
            field: "name"
        },
        {
            text: "What type of flavors do you prefer?",
            field: "taste",
            options: ["Strong", "Light", "Spicy", "Savory", "Sweet & Sour"]
        },
        {
            text: "What types of food do you like? (You can list multiple)",
            field: "favoriteFoods"
        },
        {
            text: "Are there any foods you dislike or want to avoid?",
            field: "dislikedFoods"
        },
        {
            text: "Do you have any food allergies? If yes, please specify.",
            field: "allergies"
        },
        {
            text: "What's your expected price range per meal?",
            field: "priceRange",
            options: ["£10-20", "£20-40", "£40-60", "£60-100", "Above £100"]
        },
        {
            text: "When would you prefer your delivery?",
            field: "deliveryTime",
            options: ["Breakfast (7:00-9:00)", "Lunch (11:00-13:00)", "Dinner (17:00-19:00)"]
        },
        {
            text: "What's your postal code and delivery address?",
            field: "address"
        },
        {
            text: "How many people are dining?",
            field: "numberOfDiners"
        },
        {
            text: "Great! I've noted down your preferences. I'll provide personalized recommendations based on this information. Now we can chat freely. What would you like to know?",
            options: null
        }
    ],
    userData: {
        name: "",
        taste: "",
        favoriteFoods: "",
        dislikedFoods: "",
        allergies: "",
        priceRange: "",
        deliveryTime: "",
        numberOfDiners: "1",
        address: ""
    }
};

// Conversation mode
let isFreeMode = false;

// Store conversation history
let conversationHistory = [];

// API configuration
const API_CONFIG = {
    url: "http://localhost:5001/api/chat", // Update with backend API URL
    headers: {
        "Content-Type": "application/json"
    }
};

// DOM elements
let chatMessages;
let userInput;
let sendButton;
let modeToggle;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    chatMessages = document.getElementById('chat-messages');
    userInput = document.getElementById('user-input');
    sendButton = document.getElementById('send-button');
    modeToggle = document.getElementById('mode-toggle');
    
    // Start the conversation
    setTimeout(() => {
        botAsk(chatFlow.questions[0].text);
    }, 500);
    
    // Event listeners
    sendButton.addEventListener('click', handleUserInput);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });
    
    // Mode toggle
    modeToggle.addEventListener('change', () => {
        isFreeMode = modeToggle.checked;
        if (isFreeMode && chatFlow.currentStep < chatFlow.questions.length) {
            addMessage("Now we are switching to free conversation mode. You can ask me any questions!", 'bot');
        } else if (!isFreeMode && chatFlow.currentStep >= chatFlow.questions.length) {
            addMessage("Now we are switching to guided conversation mode. I will ask you some questions to understand you.", 'bot');
            // Reset conversation flow
            chatFlow.currentStep = 0;
            chatFlow.userData = {
                name: "", taste: "", favoriteFoods: "", dislikedFoods: "", 
                allergies: "", priceRange: "", deliveryTime: "", numberOfDiners: "1", address: ""
            };
            conversationHistory = [];
            botAsk(chatFlow.questions[0].text);
        }
    });
});

// Handle user input
function handleUserInput() {
    const message = userInput.value.trim();
    if (message.length === 0) return;
    
    // Display user message
    addMessage(message, 'user');
    userInput.value = '';
    
    // Save to conversation history
    conversationHistory.push({ role: "user", content: message });
    
    if (isFreeMode) {
        // Free conversation mode: call LLM API
        sendToLLM(message);
    } else {
        // Guided mode: save user answer
        const currentQuestion = chatFlow.questions[chatFlow.currentStep];
        chatFlow.userData[currentQuestion.field] = message;
        
        // Continue conversation
        setTimeout(() => {
            continueConversation();
        }, 1000);
    }
}

// Bot asks a question
function botAsk(question) {
    // Replace template variables
    let processedQuestion = question
        .replace('{{name}}', chatFlow.userData.name || '')
        .replace(/{{interest}}/g, chatFlow.userData.interest || '');
    
    showTypingIndicator();
    
    setTimeout(() => {
        removeTypingIndicator();
        addMessage(processedQuestion, 'bot');
        
        // Save to conversation history
        conversationHistory.push({ role: "assistant", content: processedQuestion });
        
        // If current question has options, display option buttons
        const currentQuestion = chatFlow.questions[chatFlow.currentStep];
        if (currentQuestion && currentQuestion.options) {
            addOptions(currentQuestion.options);
        }
    }, 1500);
}

// Continue conversation
function continueConversation() {
    chatFlow.currentStep++;
    
    if (chatFlow.currentStep < chatFlow.questions.length) {
        botAsk(chatFlow.questions[chatFlow.currentStep].text);
    } else {
        // Guided conversation ended, switch to free mode
        isFreeMode = true;
        modeToggle.checked = true;
    }
}

// Send message to LLM API
async function sendToLLM(message) {
    showTypingIndicator();
    
    try {
        // Build request data
        const requestData = {
            messages: conversationHistory,
            user_info: chatFlow.userData
        };
        
        // Send request
        const response = await fetch(API_CONFIG.url, {
            method: "POST",
            headers: API_CONFIG.headers,
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display bot response
        removeTypingIndicator();
        addMessage(data.response, 'bot');
        
        // Save to conversation history
        conversationHistory.push({ role: "assistant", content: data.response });
        
    } catch (error) {
        console.error("API request failed:", error);
        removeTypingIndicator();
        addMessage("Sorry, I cannot connect to the language model service right now. Please try again later or check your network connection.", 'bot');
        
        // Fallback (optional)
        // fallbackResponse(message);
    }
}

// Local fallback response (optional)
function fallbackResponse(message) {
    const lowercaseMsg = message.toLowerCase();
    let response = "I'm sorry, I can only provide limited responses right now. Please try connecting to the full service later.";
    
    if (lowercaseMsg.includes("hello") || lowercaseMsg.includes("hi")) {
        response = "Hello! Nice to chat with you.";
    } else if (lowercaseMsg.includes("thank")) {
        response = "You're welcome! Happy to help!";
    } else if (lowercaseMsg.includes("bye")) {
        response = "Goodbye! Looking forward to our next conversation.";
    }
    
    addMessage(response, 'bot');
    conversationHistory.push({ role: "assistant", content: response });
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.id = 'typing-indicator';
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Add message to chat interface
function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    messageElement.textContent = text;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add option buttons
function addOptions(options) {
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container';
    
    options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-button';
        button.textContent = option;
        button.addEventListener('click', () => {
            userInput.value = option;
            handleUserInput();
            optionsContainer.remove();
        });
        
        optionsContainer.appendChild(button);
    });
    
    chatMessages.appendChild(optionsContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
} 