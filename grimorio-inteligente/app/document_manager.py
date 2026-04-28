import os
import re

from app.config import RAW_DATA_DIR
from ingestion.extract_text import process_all_pdfs
from ingestion.extract_tables import process_all_pdf_tables
from ingestion.chunking import build_chunks
from ingestion.build_index import build_vector_index


def sanitize_filename(filename):
    filename = filename.strip()
    filename = filename.replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "", filename)
    return filename


def save_uploaded_pdf(uploaded_file):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    safe_name = sanitize_filename(uploaded_file.name)

    if not safe_name.lower().endswith(".pdf"):
        raise ValueError("O arquivo precisa ser um PDF.")

    file_path = os.path.join(RAW_DATA_DIR, safe_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def process_knowledge_base():
    process_all_pdfs()
    process_all_pdf_tables()
    build_chunks()
    build_vector_index()