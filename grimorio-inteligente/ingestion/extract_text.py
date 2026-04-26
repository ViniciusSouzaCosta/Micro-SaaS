import os
import json
import fitz

from app.config import RAW_DATA_DIR, PROCESSED_DIR


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text("text")

        pages.append({
            "page": page_index + 1,
            "text": text
        })

    return pages


def process_all_pdfs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DATA_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(RAW_DATA_DIR, filename)
            print(f"Extraindo texto de: {filename}")

            pages = extract_text_from_pdf(pdf_path)

            output_name = filename.replace(".pdf", "_text.json")
            output_path = os.path.join(PROCESSED_DIR, output_name)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({
                    "source": filename,
                    "pages": pages
                }, f, ensure_ascii=False, indent=2)

            print(f"Texto salvo em: {output_path}")


if __name__ == "__main__":
    process_all_pdfs()