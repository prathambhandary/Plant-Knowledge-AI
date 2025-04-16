import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cohere API key from environment variable
cohere_api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere API client with the API key
co = cohere.Client(cohere_api_key)

def chat_with_bot(user_input, plant_name):

    preamble = f"You're a helpful assistant for plant care! Your job is to assist the user with growing and taking care of a {plant_name}. Always provide helpful advice related to the plant's health, diseases, and care, and encourage the user to engage more by asking questions like 'How's your {plant_name} doing?' or 'Is it thriving?' Keep your responses simple, clear, and in plain text—no fancy formatting, just easy-to-understand answers. Whenever you are trying to leave a line in our output, place a '<br>' tag per line to be left. USER INPUT--> "

    prompt = f"{preamble} User: {user_input}"

    # Use the "command" model for the generation
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7
    )
    
    bot_reply = response.generations[0].text.strip()
    
    return bot_reply