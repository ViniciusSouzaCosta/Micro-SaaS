import os
import json
import chromadb

from sentence_transformers import SentenceTransformer

from app.config import CHUNKS_DIR, VECTORSTORE_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME


def build_vector_index():
    chunks_path = os.path.join(CHUNKS_DIR, "chunks.json")

    if not os.path.exists(chunks_path):
        raise FileNotFoundError("Arquivo chunks.json não encontrado. Execute primeiro o chunking.py.")

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("Carregando modelo de embeddings...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Criando banco vetorial ChromaDB...")
    client = chromadb.PersistentClient(path=VECTORSTORE_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["id"])
        documents.append(chunk["content"])
        metadatas.append(chunk["metadata"])

    print("Gerando embeddings...")
    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True
    ).tolist()

    print("Salvando no ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print("Indexação concluída.")
    print(f"Total de chunks indexados: {len(ids)}")


if __name__ == "__main__":
    build_vector_index()