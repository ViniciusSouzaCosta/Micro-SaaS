import chromadb

from sentence_transformers import SentenceTransformer

from app.config import VECTORSTORE_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME, TOP_K


class Retriever:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
        self.collection = self.client.get_collection(name=COLLECTION_NAME)

    def search(self, query, category=None, top_k=TOP_K):
        query_embedding = self.embedding_model.encode(
            [query],
            normalize_embeddings=True
        ).tolist()[0]

        where_filter = None

        if category and category != "todos":
            where_filter = {
                "category": category
            }

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