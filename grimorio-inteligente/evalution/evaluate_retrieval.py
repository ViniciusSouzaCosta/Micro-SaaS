import json

from app.retriever import Retriever


def evaluate():
    with open("evaluation/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    retriever = Retriever()

    total = len(questions)
    hit_at_3 = 0
    hit_at_5 = 0

    for item in questions:
        question = item["question"]
        expected_keyword = item["expected_keyword"].lower()

        results = retriever.search(question, top_k=5)

        top_3_text = " ".join([r["content"].lower() for r in results[:3]])
        top_5_text = " ".join([r["content"].lower() for r in results[:5]])

        found_at_3 = expected_keyword in top_3_text
        found_at_5 = expected_keyword in top_5_text

        if found_at_3:
            hit_at_3 += 1

        if found_at_5:
            hit_at_5 += 1

        print("=" * 80)
        print(f"Pergunta: {question}")
        print(f"Palavra esperada: {expected_keyword}")
        print(f"Acertou@3: {found_at_3}")
        print(f"Acertou@5: {found_at_5}")

    precision_at_3 = hit_at_3 / total
    precision_at_5 = hit_at_5 / total

    print("\nResultado final:")
    print(f"Precisão@3: {precision_at_3:.2f}")
    print(f"Precisão@5: {precision_at_5:.2f}")


if __name__ == "__main__":
    evaluate()