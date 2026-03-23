"""
Purpose:
Handles all interactions with Groq LLM.
Provides a clean interface for generating responses.
"""

from groq import Groq
from app.core.config import settings

# Initialize client once (singleton style)
client = Groq(api_key=settings.GROQ_API_KEY)


def generate_response(prompt: str) -> str:
    """
    Sends prompt to Groq LLM and returns response text.

    Args:
        prompt (str): Input prompt for LLM

    Returns:
        str: Generated response
    """
    
    try:
        completion = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature = 0.7
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error generating response : {str(e)}"


