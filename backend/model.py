from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def process_text_with_model(extracted_text):
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "You're a project Manager."},
            {"role": "user", "content": extracted_text + "\nSummarize this"}
        ]
    )
    return response.choices[0].message.content
