import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os

def gemini_response(query: str, vectorDB_responses) -> str:

    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f'''
        User's Query - {query}
        Relevant Response received from Vector Database - {vectorDB_responses}
        You need to filter out the exact answer of the user query and frame the exact response into complete sentences.
    ''')

    return response