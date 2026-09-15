import numpy as np

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

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
    print("LangChain Chroma.from_documents Test")
    print("=" * 60)

    embeddings = get_embeddings()

    document = Document(
        page_content=TEXT,
        metadata={
            "question": TEXT,
        },
    )

    print("\nCreating Chroma from document...")

    vectorstore = Chroma.from_documents(
        documents=[document],
        embedding=embeddings,
    )

    print("Document inserted.")

    result = vectorstore.get(
        include=["documents", "embeddings"]
    )

    stored_embedding = np.array(
        result["embeddings"][0]
    )

    query_embedding = np.array(
        embeddings.embed_query(TEXT)
    )

    print("\nQuery embedding:")
    print(query_embedding[:10])
    print(f"Dimension: {len(query_embedding)}")

    print("\nStored embedding:")
    print(stored_embedding[:10])
    print(f"Dimension: {len(stored_embedding)}")

    similarity = cosine_similarity(
        query_embedding,
        stored_embedding,
    )

    distance = np.linalg.norm(
        query_embedding - stored_embedding
    )

    print("\nComparison:")
    print(f"Cosine similarity: {similarity:.6f}")
    print(f"Euclidean distance: {distance:.6f}")


if __name__ == "__main__":
    main()