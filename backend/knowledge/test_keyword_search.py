from knowledge.vectorstore import get_chroma_collection


query = "新创建的仓库为什么看不到库存"

collection = get_chroma_collection()

results = collection.get(
    include=[
        "documents",
        "metadatas",
    ]
)

print("=" * 60)
print("Keyword Search Test")
print("=" * 60)

for document, metadata in zip(
    results["documents"],
    results["metadatas"],
):

    question = metadata.get(
        "question",
        "",
    )

    if (
        "仓库" in question
        or "库存" in question
    ):
        print("\nQuestion:")
        print(question)

        print("\nKeywords:")
        print(
            metadata.get(
                "keywords",
                "",
            )
        )

        print("\nDocument:")
        print(document)

        print("-" * 60)