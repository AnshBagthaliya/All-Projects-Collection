import random
import json
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Load response data
with open("responses.json", "r") as file:
    data = json.load(file)

# Preprocess user input
def preprocess(user_input):
    return [word.lower() for word in word_tokenize(user_input)]

# Generate response
def get_response(user_input):
    tokens = preprocess(user_input)
    
    # Greeting
    if any(word in data["greetings"] for word in tokens):
        return random.choice(data["greeting_responses"])
    
    # Farewell
    elif any(word in data["farewells"] for word in tokens):
        return random.choice(data["farewell_responses"])
    
    # Thanks
    elif any(word in data["thanks"] for word in tokens):
        return random.choice(data["thanks_responses"])
    
    # Default
    else:
        return "I'm not sure how to respond to that. Can you ask something else? 🤔"

# Chat loop
def chat():
    print("🤖 Human-like Chatbot: Hello! Type something to begin or type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Bot:", random.choice(data["farewell_responses"]))
            break
        response = get_response(user_input)
        print("Bot:", response)

# Run chatbot
if __name__ == "__main__":
    chat()
