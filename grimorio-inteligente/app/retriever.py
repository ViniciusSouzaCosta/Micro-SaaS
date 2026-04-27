import chromadb
from sentence_transformers import SentenceTransformer
from app.config import VECTORSTORE_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME, TOP_K

# ⭐ Singleton para o modelo de embeddings (carrega UMA vez)
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("🔄 Carregando modelo de embeddings...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("✅ Modelo de embeddings carregado!")
    return _embedding_model

# ⭐ Singleton para o cliente ChromaDB
_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _client is None:
        print("🔄 Conectando ao ChromaDB...")
        _client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
        _collection = _client.get_collection(name=COLLECTION_NAME)
        print("✅ ChromaDB conectado!")
    return _collection

class Retriever:
    def __init__(self):
        # ⭐ Agora usa singletons - não recarrega!
        self.embedding_model = get_embedding_model()
        self.collection = get_collection()

    def search(self, query, category=None, top_k=TOP_K):
        query_embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True
        ).tolist()[0]

        where_filter = None
        if category and category != "todos":
            where_filter = {"category": category}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )

        retrieved = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc, metadata, distance in zip(documents, metadatas, distances):
            retrieved.append({
                "content": doc,
                "metadata": metadata,
                "distance": distance
            })

        return retrieved