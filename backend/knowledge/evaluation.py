import json
from pathlib import Path

from knowledge.retrieval import retrieve_documents


DATA_PATH = (
    Path(__file__).parent
    / "data"
    / "evaluation_cases.json"
)


def load_cases():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate():
    cases = load_cases()

    total = len(cases)
    answerable_cases = [
        case for case in cases
        if case["has_answer"]
    ]
    unanswerable_cases = [
        case for case in cases
        if not case["has_answer"]
    ]

    top1_correct = 0
    top3_correct = 0

    answerable_top1 = 0
    answerable_top3 = 0

    unanswerable_false_positive = 0

    print("=" * 70)
    print("RAG Retrieval Evaluation")
    print("=" * 70)

    for index, case in enumerate(cases, start=1):
        query = case["query"]
        expected_question = case["expected_question"]
        has_answer = case["has_answer"]

        results = retrieve_documents(
            query,
            k=30,
            top_k=3,
        )

        retrieved_questions = [
            result["metadata"].get("question", "")
            for result in results
        ]

        top1_match = (
            len(retrieved_questions) > 0
            and retrieved_questions[0] == expected_question
        )

        top3_match = (
            expected_question in retrieved_questions
        )

        if has_answer:
            if top1_match:
                top1_correct += 1
                answerable_top1 += 1

            if top3_match:
                top3_correct += 1
                answerable_top3 += 1
        else:
            # For unanswerable questions, there should be
            # no expected answer in the knowledge base.
            # We record whether retrieval still returned
            # potentially misleading results.
            if results:
                unanswerable_false_positive += 1

        print(f"\n[{index}/{total}]")
        print(f"Query: {query}")
        print(f"Expected: {expected_question}")
        print(f"Has answer: {has_answer}")

        for rank, result in enumerate(results, start=1):
            question = result["metadata"].get(
                "question",
                ""
            )
            score = result["score"]

            marker = ""

            if question == expected_question:
                marker = " <-- MATCH"

            print(
                f"  {rank}. "
                f"score={score:.6f} "
                f"{question}{marker}"
            )

    top1_accuracy = (
        top1_correct / len(answerable_cases)
        if answerable_cases
        else 0
    )

    top3_recall = (
        top3_correct / len(answerable_cases)
        if answerable_cases
        else 0
    )

    answerable_top1_rate = (
        answerable_top1 / len(answerable_cases)
        if answerable_cases
        else 0
    )

    answerable_top3_rate = (
        answerable_top3 / len(answerable_cases)
        if answerable_cases
        else 0
    )

    false_positive_rate = (
        unanswerable_false_positive / len(unanswerable_cases)
        if unanswerable_cases
        else 0
    )

    print("\n" + "=" * 70)
    print("Evaluation Results")
    print("=" * 70)

    print(
        f"\nTotal cases: {total}"
    )

    print(
        f"Answerable cases: "
        f"{len(answerable_cases)}"
    )

    print(
        f"Unanswerable cases: "
        f"{len(unanswerable_cases)}"
    )

    print(
        f"\nTop-1 Accuracy: "
        f"{top1_accuracy:.2%}"
    )

    print(
        f"Top-3 Recall: "
        f"{top3_recall:.2%}"
    )

    print(
        f"\nAnswerable Top-1: "
        f"{answerable_top1_rate:.2%}"
    )

    print(
        f"Answerable Top-3: "
        f"{answerable_top3_rate:.2%}"
    )

    print(
        f"\nUnanswerable False Positive Rate: "
        f"{false_positive_rate:.2%}"
    )


if __name__ == "__main__":
    evaluate()