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
        You need to frame this response into complete sentences.
        Ensure that the exact meaning of response does not change and try to make only lil modifications in the response.
        Also if the query is present in the response, try to frame response as an answer of query but not displaying the query as it is.
    ''')

    return response