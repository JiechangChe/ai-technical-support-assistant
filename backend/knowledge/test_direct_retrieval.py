from knowledge.retrieval import retrieve_documents


query = "新创建的仓库为什么看不到库存"


results = retrieve_documents(
    query,
    k=30,
    top_k=3,
)


print("=" * 60)
print("Hybrid Retrieval Test")
print("=" * 60)

print(f"\nQuery: {query}")

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"\n{index}. "
        f"score={result['score']:.6f}"
    )

    print(
        "Question:",
        result["metadata"].get(
            "question",
            "",
        ),
    )

    print(
        "Answer:",
        result["document"],
    )