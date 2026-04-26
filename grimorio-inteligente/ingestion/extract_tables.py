import os
import json
import pdfplumber

from app.config import RAW_DATA_DIR, PROCESSED_DIR


def table_to_markdown(table):
    if not table:
        return ""

    header = table[0]
    rows = table[1:]

    header = [str(cell).strip() if cell else "" for cell in header]

    markdown = "| " + " | ".join(header) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"

    for row in rows:
        clean_row = [str(cell).strip() if cell else "" for cell in row]
        markdown += "| " + " | ".join(clean_row) + " |\n"

    return markdown


def extract_tables_from_pdf(pdf_path):
    tables_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_index, table in enumerate(tables):
                markdown = table_to_markdown(table)

                if markdown.strip():
                    tables_data.append({
                        "page": page_index + 1,
                        "table_index": table_index + 1,
                        "markdown": markdown
                    })

    return tables_data


def process_all_pdf_tables():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DATA_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(RAW_DATA_DIR, filename)
            print(f"Extraindo tabelas de: {filename}")

            tables = extract_tables_from_pdf(pdf_path)

            output_name = filename.replace(".pdf", "_tables.json")
            output_path = os.path.join(PROCESSED_DIR, output_name)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({
                    "source": filename,
                    "tables": tables
                }, f, ensure_ascii=False, indent=2)

            print(f"Tabelas salvas em: {output_path}")


if __name__ == "__main__":
    process_all_pdf_tables()