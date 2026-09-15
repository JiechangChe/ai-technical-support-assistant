import json
from pathlib import Path
from knowledge.retrieval import retrieve_documents
from ai.judge import judge_answerability


DATA_PATH = (
    Path(__file__).parent
    / "data"
    / "evaluation_cases.json"
)


def main():
    with open(
        DATA_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        cases = json.load(f)

    correct = 0
    evaluated = 0

    print("=" * 70)
    print("LLM Answerability Evaluation")
    print("=" * 70)

    for index, case in enumerate(cases, start=1):
        query = case["query"]
        expected_answerable = case["has_answer"]

        print("\n" + "=" * 70)
        print(f"Case {index}")
        print("=" * 70)

        print(f"\nQuery:\n{query}")

        documents = retrieve_documents(
            query,
            k=30,
            top_k=3,
        )

        print("\nTop retrieved knowledge:")

        for rank, document in enumerate(
            documents,
            start=1,
        ):
            question = document["metadata"].get(
                "question",
                "",
            )

            print(
                f"\n{rank}. "
                f"score={document['score']:.6f}"
            )
            print(f"Question: {question}")

        result = judge_answerability(
            query,
            documents,
        )

        predicted_answerable = result.get(
            "answerable"
        )

        reason = result.get(
            "reason",
            "",
        )

        print(
            f"\nExpected: "
            f"{expected_answerable}"
        )

        print(
            f"LLM Judge: "
            f"{predicted_answerable}"
        )

        print(
            f"Reason: "
            f"{reason}"
        )

        if predicted_answerable is not None:
            evaluated += 1

            if (
                predicted_answerable
                == expected_answerable
            ):
                correct += 1
                print("Result: CORRECT")
            else:
                print("Result: WRONG")
        else:
            print("Result: INVALID JSON")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print(f"Evaluated cases: {evaluated}")

    if evaluated > 0:
        accuracy = correct / evaluated
        print(
            f"LLM Judge Accuracy: "
            f"{accuracy:.2%}"
        )


if __name__ == "__main__":
    main()