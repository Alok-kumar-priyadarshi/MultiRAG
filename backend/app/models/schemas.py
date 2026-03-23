"""
Purpose:
Defines request/response schemas for API validation.
"""

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    query: Optional[str] = None
    url: Optional[str] = None
    
    
class ChatResponse(BaseModel):
    answer: str
    input_type: str