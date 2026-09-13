from knowledge.retrieval import retrieve_documents


def main():
    query = "客户交易条款审批不了"

    docs = retrieve_documents(
        query,
        k=20,
    )

    print(f"\nQuery: {query}")
    print(f"Retrieved documents: {len(docs)}")

    for i, doc in enumerate(docs, start=1):
        print("\n" + "=" * 60)
        print(f"Document {i}")
        print("=" * 60)
        print(doc.page_content)


if __name__ == "__main__":
    main()