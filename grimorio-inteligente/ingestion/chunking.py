import os
import json
import re

from app.config import PROCESSED_DIR, CHUNKS_DIR


def clean_text(text):
    text = text.replace("\n\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text_into_chunks(text, max_chars=1800, overlap=250):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + max_chars
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

        if start < 0:
            start = 0

        if start >= text_length:
            break

    return chunks


def guess_category(text):
    lower = text.lower()

    if "spell" in lower or "casting time" in lower or "range:" in lower:
        return "magia"

    if "weapon" in lower or "armor" in lower or "equipment" in lower:
        return "equipamento"

    if "condition" in lower or "paralyzed" in lower or "frightened" in lower:
        return "condicao"

    if "combat" in lower or "attack roll" in lower or "initiative" in lower:
        return "combate"

    if "monster" in lower or "challenge" in lower:
        return "monstro"

    return "regra_geral"


def create_text_chunks():
    os.makedirs(CHUNKS_DIR, exist_ok=True)

    all_chunks = []
    chunk_id = 1

    for filename in os.listdir(PROCESSED_DIR):
        if filename.endswith("_text.json"):
            path = os.path.join(PROCESSED_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            source = data["source"]

            for page_data in data["pages"]:
                page = page_data["page"]
                text = clean_text(page_data["text"])

                if not text:
                    continue

                page_chunks = split_text_into_chunks(text)

                for chunk in page_chunks:
                    all_chunks.append({
                        "id": f"text_{chunk_id}",
                        "content": chunk,
                        "metadata": {
                            "source": source,
                            "page": page,
                            "content_type": "text",
                            "category": guess_category(chunk)
                        }
                    })

                    chunk_id += 1

    return all_chunks


def create_table_chunks():
    all_chunks = []
    chunk_id = 1

    for filename in os.listdir(PROCESSED_DIR):
        if filename.endswith("_tables.json"):
            path = os.path.join(PROCESSED_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            source = data["source"]

            for table_data in data["tables"]:
                page = table_data["page"]
                table_index = table_data["table_index"]
                markdown = table_data["markdown"]

                all_chunks.append({
                    "id": f"table_{chunk_id}",
                    "content": markdown,
                    "metadata": {
                        "source": source,
                        "page": page,
                        "content_type": "table",
                        "category": guess_category(markdown),
                        "table_index": table_index
                    }
                })

                chunk_id += 1

    return all_chunks


def build_chunks():
    text_chunks = create_text_chunks()
    table_chunks = create_table_chunks()

    all_chunks = text_chunks + table_chunks

    output_path = os.path.join(CHUNKS_DIR, "chunks.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Total de chunks criados: {len(all_chunks)}")
    print(f"Arquivo salvo em: {output_path}")


if __name__ == "__main__":
    build_chunks()