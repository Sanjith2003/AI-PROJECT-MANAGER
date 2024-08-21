import json
from llamaapi import LlamaAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")

# Initialize the SDK
llama = LlamaAPI(api_key)

def process_text_with_model(extracted_text):
    # Build the API request with constraints
    api_request_json = {
        "messages": [
            {"role": "system", "content": "You're a DBMS Teacher."},
            {"role": "user", "content": extracted_text + "\nExplain this in detail"}
        ],
        "max_tokens": 1000,  # Maximum number of tokens in the response
        "temperature": 0.1,  # Controls randomness in the output
        "top_p": 1.0,        # Nucleus sampling
        "frequency_penalty": 1.0,  # Penalizes new tokens based on their frequency in the text so far
        "stream": False      # Disable streaming
    }

    # Execute the request
    response = llama.run(api_request_json)
    
    # Return the content of the response
    return response.json()["choices"][0]["message"]["content"]

