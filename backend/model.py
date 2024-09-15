import requests
import os
from dotenv import load_dotenv
from markdown2 import markdown  # Use markdown library to convert text

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("API_KEY")

# Set the API endpoint for Gemini
API_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

# Initialize headers including Content-Type
headers = {
    'Content-Type': 'application/json',
}

def process_text_with_gemini(extracted_text):
    # Define the prompt to send to Gemini
    prompt = "Generate a complete project plan for the following SRS document, let the plan include different modules, technology stack for each module, time to spend in each module, total time, total number of employees in each module, etc."

    # Build the request data payload
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": extracted_text + "\n" + prompt
                    }
                ]
            }
        ]
    }

    # Execute the API request to Gemini
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        
        # Extract the core content (text) from the response
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Convert the markdown content to HTML or render properly in markdown
            formatted_content = markdown(content)  # Converts markdown to HTML
            return formatted_content
        else:
            return "No content generated."
    else:
        print(f"Failed to get response, status code: {response.status_code}")
        print(response.text)
        return None
