
# from app.utils.embeddings import get_embeddings
# from app.db.vector_store import search, index
# from app.core.groq_client import generate_response
# from app.services.memory_service import get_history


# # 🔹 Detect summary intent
# def is_summary_query(query: str) -> bool:
#     keywords = ["summarize", "summary", "summarise", "explain document"]
#     return any(k in query.lower() for k in keywords)


# def generate_rag_response(query: str, session_id: str, top_k: int = 10):

#     try:
#         # 🔹 Get memory (limit to last 3 exchanges to avoid noise)
#         history = get_history(session_id)[-6:]

#         history_text = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in history]
#         )

#         # 🔴 CASE 1: No data → fallback (clean chatbot mode)
#         if index.ntotal == 0:
#             fallback_prompt = f"""
#             You are a helpful AI assistant.

#             Answer the user's question clearly and concisely.

#             Question:
#             {query}
#             """
#             response = generate_response(fallback_prompt)

#             return {"answer": response, "sources": []}

#         # 🔹 Embed query
#         embeddings = get_embeddings([query])
#         query_embedding = embeddings[0]

#         # 🔹 Retrieve relevant chunks
#         retrieved_chunks = search(query_embedding, top_k=top_k)

#         # 🔴 CASE 2: No relevant chunks → fallback
#         if not retrieved_chunks:
#             fallback_prompt = f"""
#             You are a helpful AI assistant.

#             Answer the user's question based on general knowledge.

#             Question:
#             {query}
#             """
#             response = generate_response(fallback_prompt)

#             return {"answer": response, "sources": []}

#         # 🔹 Build context
#         context = "\n".join(retrieved_chunks)

#         # 🔴 CASE 3: SUMMARY MODE (important fix)
#         if is_summary_query(query):
#             prompt = f"""
#             You are a document summarization assistant.

#             Summarize the following content clearly and concisely.

#             Context:
#             {context}

#             Summary:
#             """

#         # 🔹 NORMAL QA MODE
#         else:
#             prompt = f"""
#             You are a strict document assistant.

#             Answer ONLY using the provided context.

#             If the answer is not in the context:
#             say "I don't know based on the provided document."

#             Conversation History:
#             {history_text}

#             Context:
#             {context}

#             Question:
#             {query}

#             Answer:
#             """

#         # 🔹 Generate response
#         response = generate_response(prompt)

#         return {
#             "answer": response,
#             "sources": retrieved_chunks
#         }

#     except Exception as e:
#         return {"answer": f"Error: {str(e)}", "sources": []}

"""
Purpose:
Handles full conversational RAG pipeline:
Query → Rewrite → Retrieve → Context + Memory → LLM → Answer
"""

from app.utils.embeddings import get_embeddings
from app.db.vector_store import search, index, stored_texts
from app.core.groq_client import generate_response
from app.services.memory_service import get_history


# 🔹 Detect summary intent
def is_summary_query(query: str) -> bool:
    keywords = ["summarize", "summary", "summarise", "explain document"]
    return any(k in query.lower() for k in keywords)


def generate_rag_response(query: str, session_id: str, top_k: int = 10):

    try:
        # 🔹 Step 1: Get memory (last 5 messages)
        history = get_history(session_id)[-5:]

        history_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in history]
        )

        # 🔥 Step 2: Rewrite query using memory (IMPORTANT)
        if history:
            last_user_msg = next(
                (msg["content"] for msg in reversed(history) if msg["role"] == "user"),
                ""
            )

            # Avoid repeating same query
            if last_user_msg and last_user_msg != query:
                query = f"{last_user_msg} -> {query}"

        # 🔴 CASE 1: No documents → chatbot mode
        if index.ntotal == 0:
            fallback_prompt = f"""
            You are a helpful conversational AI assistant.

            Conversation History:
            {history_text}

            User Question:
            {query}

            Answer:
            """
            response = generate_response(fallback_prompt)

            return {"answer": response, "sources": []}

        # 🔹 Step 3: Embed query
        embeddings = get_embeddings([query])
        query_embedding = embeddings[0]

        # 🔹 Step 4: Retrieve chunks
        retrieved_chunks = search(query_embedding, top_k=top_k)

        # 🔴 CASE 2: No relevant chunks
        if not retrieved_chunks:
            fallback_prompt = f"""
            You are a helpful conversational AI assistant.

            Conversation History:
            {history_text}

            Answer the user's question using general knowledge.

            Question:
            {query}

            Answer:
            """
            response = generate_response(fallback_prompt)

            return {"answer": response, "sources": []}

        # 🔹 Step 5: Build context
        context = "\n".join(retrieved_chunks)

        # 🔴 CASE 3: Summary mode
        if is_summary_query(query):
            # If retrieval weak → fallback to full doc
            if not retrieved_chunks:
                context = "\n".join(stored_texts[:20])

            prompt = f"""
            You are a document summarization assistant.

            Summarize the following content clearly and concisely.

            Conversation History:
            {history_text}

            Context:
            {context}

            Summary:
            """

        # 🔹 NORMAL conversational RAG
        else:
            prompt = f"""
            You are an intelligent AI assistant.

            You can use:
            - Conversation history
            - Retrieved document context

            Rules:
            - If question refers to previous conversation → use history
            - If question refers to document → use context
            - If both → combine them
            - If unclear → answer naturally

            Conversation History:
            {history_text}

            Document Context:
            {context}

            User Question:
            {query}

            Answer:
            """

        # 🔹 Step 6: Generate response
        response = generate_response(prompt)

        return {
            "answer": response,
            "sources": retrieved_chunks
        }

    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": []}