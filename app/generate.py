import os

from dotenv import load_dotenv
from google import genai

from retrieve import retrieve

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

question = input("\n Ask a question: ")

results = retrieve(question)

documents = results["documents"][0]

context = "\n\n---\n\n".join(documents)

prompt = f""" 
        You are an engineering knowledge assistant. 

        Answer the question using only the provided context.

        If the context does not contain enough information to answer the question,
        say that the available documentation does not contain enough information.

        Context: 
        {context}

        Question: 
        {question}

        Answer:
    """

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print("\n--- Answer ---\n")
print(response.text)