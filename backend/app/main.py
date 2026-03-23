"""
Purpose:
Main entry point of the FastAPI application.
Initializes app and includes all routes.
"""

from fastapi import FastAPI
from app.api.chat_routes import router as chat_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Multi-Source RAG Backend",
    description="Handles PDF, URL, YouTube and query-based RAG",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat_router, prefix="/api")
