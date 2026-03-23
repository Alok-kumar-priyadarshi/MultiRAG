"""
Purpose:
Central configuration management.
Loads environment variables and makes them accessible across the app.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    sentence_transformer_model:str = os.getenv("SENTENCE_TRANSFORMER_MODEL")

settings = Settings()