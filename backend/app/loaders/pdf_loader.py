"""
Purpose:
Extracts text from PDF files.
"""

from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()

            print(f"[DEBUG] Page {i} text length:", len(page_text) if page_text else 0)

            text += page_text or ""

        print("[DEBUG] Total extracted length:", len(text))

        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    