from nemoguardrails import LLMRails, RailsConfig
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

rails_config = RailsConfig.from_path("config")  

rails=LLMRails(rails_config)

new_message = rails.generate(messages=[{
    "role": "user",
    "content": "Hello! What can you do for me?"
}])

print(new_message)