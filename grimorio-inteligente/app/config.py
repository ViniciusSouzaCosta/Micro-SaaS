import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore", "chroma_db")

COLLECTION_NAME = "grimorio_rpg"

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

LLM_MODEL_NAME = "llama3.1:8b"

TOP_K = 5