import ollama

from app.config import LLM_MODEL_NAME
from app.prompts import SYSTEM_PROMPT


def build_context(retrieved_chunks):
    context_parts = []

    for index, item in enumerate(retrieved_chunks, start=1):
        metadata = item["metadata"]
        content = item["content"]

        source = metadata.get("source", "Fonte desconhecida")
        page = metadata.get("page", "N/A")
        category = metadata.get("category", "N/A")
        content_type = metadata.get("content_type", "N/A")

        context_parts.append(
            f"[Trecho {index}]\n"
            f"Fonte: {source}\n"
            f"Página: {page}\n"
            f"Categoria: {category}\n"
            f"Tipo: {content_type}\n"
            f"Conteúdo:\n{content}\n"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, retrieved_chunks):
    context = build_context(retrieved_chunks)

    user_prompt = f"""
Contexto recuperado:
{context}

Pergunta do usuário:
{question}

Resposta:
"""

    response = ollama.chat(
        model=LLM_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response["message"]["content"]