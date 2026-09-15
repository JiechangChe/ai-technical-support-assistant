import numpy as np
import chromadb

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TEXT = "新创建的仓库为什么看不到库存"


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def main():

    print("=" * 60)
    print("Raw Chroma Embedding Test")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Generate embedding directly
    # --------------------------------------------------

    model = SentenceTransformer(MODEL_NAME)

    embedding = model.encode(TEXT).tolist()

    print("\nOriginal embedding:")
    print(embedding[:10])

    print(
        f"Embedding dimension: {len(embedding)}"
    )

    # --------------------------------------------------
    # 2. Create a completely fresh Chroma client
    # --------------------------------------------------

    client = chromadb.Client()

    collection = client.create_collection(
        name="embedding_debug"
    )

    # --------------------------------------------------
    # 3. Insert document + our own embedding
    # --------------------------------------------------

    collection.add(
        ids=["test-1"],
        documents=[TEXT],
        embeddings=[embedding],
    )

    print("\nDocument inserted.")

    # --------------------------------------------------
    # 4. Read embedding back
    # --------------------------------------------------

    result = collection.get(
        ids=["test-1"],
        include=[
            "documents",
            "embeddings",
        ],
    )

    stored_embedding = np.array(
        result["embeddings"][0]
    )

    print("\nStored embedding:")
    print(stored_embedding[:10])

    print(
        f"Stored dimension: "
        f"{len(stored_embedding)}"
    )

    # --------------------------------------------------
    # 5. Compare
    # --------------------------------------------------

    similarity = cosine_similarity(
        embedding,
        stored_embedding,
    )

    distance = np.linalg.norm(
        np.array(embedding)
        - stored_embedding
    )

    print("\nComparison:")
    print(
        f"Cosine similarity: "
        f"{similarity:.6f}"
    )

    print(
        f"Euclidean distance: "
        f"{distance:.6f}"
    )


if __name__ == "__main__":
    main()