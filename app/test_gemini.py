import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f""" 
        You are an engineering knowledge assistant. 

        Use only the provided context to answer the question. 
        If the context does not contain the answer, say so. 

        CONTEXT: 
        {retrieved_context}

        QUESTION: 
        {question}
    """
)

print(response.text)