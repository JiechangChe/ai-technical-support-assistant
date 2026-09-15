import numpy as np

from knowledge.vectorstore import get_vectorstore
from knowledge.vectorstore import get_embeddings


TEXT = "新创建的仓库为什么看不到库存"


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def main():
    print("=" * 60)
    print("Persistent Chroma Test")
    print("=" * 60)

    # 1. Load existing persistent Chroma
    vectorstore = get_vectorstore()

    print("\nCollection:")
    print(vectorstore._collection.name)

    print("\nDocument count:")
    print(vectorstore._collection.count())

    # 2. Find exact document
    result = vectorstore.get(
        where={
            "question": TEXT
        },
        include=[
            "documents",
            "metadatas",
            "embeddings",
        ],
    )

    print("\nExact document count:")
    print(len(result["documents"]))

    if not result["documents"]:
        print("ERROR: Exact document not found.")
        return

    # 3. Stored embedding
    stored_embedding = np.array(
        result["embeddings"][0]
    )

    # 4. Generate query embedding
    embeddings = get_embeddings()

    query_embedding = np.array(
        embeddings.embed_query(TEXT)
    )

    print("\nStored embedding:")
    print(stored_embedding[:10])

    print("\nQuery embedding:")
    print(query_embedding[:10])

    print("\nDimensions:")
    print("Stored:", len(stored_embedding))
    print("Query :", len(query_embedding))

    # 5. Compare
    similarity = cosine_similarity(
        query_embedding,
        stored_embedding,
    )

    distance = np.linalg.norm(
        query_embedding - stored_embedding
    )

    print("\nEmbedding comparison:")
    print(f"Cosine similarity: {similarity:.6f}")
    print(f"Euclidean distance: {distance:.6f}")

    # 6. Actual similarity search
    print("\n" + "=" * 60)
    print("Actual similarity_search")
    print("=" * 60)

    docs = vectorstore.similarity_search_with_score(
        TEXT,
        k=30,
    )

    found = False

    for i, (doc, score) in enumerate(docs, start=1):
        question = doc.metadata.get(
            "question",
            "",
        )

        print(
            f"{i:02d}. score={score:.6f} | "
            f"{question}"
        )

        if question == TEXT:
            found = True

    print("\nExact document in Top 30:", found)


if __name__ == "__main__":
    main()