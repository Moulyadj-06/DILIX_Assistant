
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_api = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api)

def get_llm_response(prompt: str) -> str:
    """
    Get AI response dynamically from Groq LLM.
    """
    # Add a system prompt that defines DILIX behavior
    system_prompt = (
        "You are DILIX, an AI assistant. "
        "Answer the user's question clearly, concisely, and politely. "
        "Do not hallucinate; if you don't know the answer, say 'I don't know'. "
        "Only introduce yourself if explicitly asked."
    )

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=512
    )

    return completion.choices[0].message.content.strip()
