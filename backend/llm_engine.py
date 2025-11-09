
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_api = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api)

def get_llm_response(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=512
    )
    # Access the content correctly
    return completion.choices[0].message.content
