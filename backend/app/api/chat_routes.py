
"""
Purpose:
Main chat endpoint integrating routing, ingestion, RAG, and conversational memory.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import shutil

from app.services.router_service import classify_input
from app.services.ingestion_service import ingest_data
from app.services.rag_service import generate_rag_response
from app.core.groq_client import generate_response
from app.services.memory_service import add_message
from app.db.vector_store import reset_index

router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/chat")
def chat(
    query: str = Form(None),
    url: str = Form(None),
    file: UploadFile = File(None),
    session_id: str = Form("default")
):
    """
    Unified chat endpoint handling:
    - Text queries
    - PDF uploads
    - URLs
    - YouTube links
    - Conversational memory
    """

    try:
        # 🔹 Step 1: Classify input
        input_type = classify_input(query=query, url=url, file=file)

        # 🔹 Step 2: Handle ingestion

        # 📄 PDF
        if input_type == "PDF" and file:
            file_path = os.path.join(TEMP_DIR, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            ingest_data("PDF", file_path)

            if os.path.exists(file_path):
                os.remove(file_path)

            # If no query → guide user
            if not query:
                return {
                    "answer": "PDF uploaded successfully. You can now ask questions about it.",
                    "sources": [],
                    "input_type": input_type
                }

        # 🌐 URL
        elif input_type == "URL" and url:
            ingest_data("URL", url)

            if not query:
                return {
                    "answer": "URL processed successfully. Ask a question about the content.",
                    "sources": [],
                    "input_type": input_type
                }

        # ▶️ YOUTUBE
        elif input_type == "YOUTUBE" and url:
            result = ingest_data("YOUTUBE", url)

            if not result or "error" in result:
                answer = generate_response(query or "Summarize this video")

                # Save memory
                if query:
                    add_message(session_id, "user", query)
                add_message(session_id, "assistant", answer)

                return {
                    "answer": answer,
                    "sources": [],
                    "input_type": input_type,
                    "note": "No transcript available, used general LLM knowledge"
                }

            if not query:
                return {
                    "answer": "Video processed successfully. Ask a question about it.",
                    "sources": [],
                    "input_type": input_type
                }

        # 📝 TEXT
        elif input_type == "TEXT":
            if not query:
                return {
                    "answer": "Please provide a query.",
                    "sources": [],
                    "input_type": input_type
                }

        # 🔹 Step 3: Generate response (RAG + Memory)

        rag_result = generate_rag_response(query, session_id)

        if not isinstance(rag_result, dict):
            rag_result = {
                "answer": str(rag_result),
                "sources": []
            }

        # 🔹 Step 4: Save memory AFTER response
        add_message(session_id, "user", query)
        add_message(session_id, "assistant", rag_result["answer"])

        return {
            "answer": rag_result["answer"],
            "sources": rag_result.get("sources", []),
            "input_type": input_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
def reset():
    """
    Resets FAISS vector store.
    """
    reset_index()
    return {"message": "Vector store reset successful"}
