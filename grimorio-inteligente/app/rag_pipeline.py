from app.retriever import Retriever
from app.generator import generate_answer


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()

    def ask(self, question, category="todos", top_k=5):
        retrieved_chunks = self.retriever.search(
            query=question,
            category=category,
            top_k=top_k
        )

        answer = generate_answer(question, retrieved_chunks)

        return {
            "answer": answer,
            "sources": retrieved_chunks
        }