from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = Path(__file__).parent / "test_chroma_persistent"


TEXT = "新创建的仓库为什么看不到库存"


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5

    return dot / (norm_a * norm_b)


def euclidean_distance(a, b):
    return sum(
        (x - y) ** 2
        for x, y in zip(a, b)
    ) ** 0.5


print("=" * 60)
print("Raw Persistent Chroma Test")
print("=" * 60)


# --------------------------------------------------
# 1. Load embedding model
# --------------------------------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 2. Generate embedding
# --------------------------------------------------

embedding = model.encode(TEXT).tolist()

print("\nOriginal embedding:")
print(embedding[:10])

print("Dimension:")
print(len(embedding))


# --------------------------------------------------
# 3. Create persistent Chroma
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


collection = client.get_or_create_collection(
    name="test_collection"
)


# --------------------------------------------------
# 4. Clear old data
# --------------------------------------------------

try:
    collection.delete(ids=["test-document"])
except Exception:
    pass


# --------------------------------------------------
# 5. Add document manually
# --------------------------------------------------

collection.add(
    ids=["test-document"],
    documents=[TEXT],
    embeddings=[embedding],
)


print("\nDocument added.")


# --------------------------------------------------
# 6. Read it back
# --------------------------------------------------

result = collection.get(
    ids=["test-document"],
    include=["documents", "embeddings"],
)


stored_embedding = result["embeddings"][0]


print("\nStored embedding:")
print(stored_embedding[:10])

print("\nStored dimension:")
print(len(stored_embedding))


# --------------------------------------------------
# 7. Compare
# --------------------------------------------------

cosine = cosine_similarity(
    embedding,
    stored_embedding,
)

euclidean = euclidean_distance(
    embedding,
    stored_embedding,
)


print("\nComparison:")
print(f"Cosine similarity: {cosine:.6f}")
print(f"Euclidean distance: {euclidean:.6f}")


# --------------------------------------------------
# 8. Search
# --------------------------------------------------

results = collection.query(
    query_embeddings=[embedding],
    n_results=1,
)


print("\nSimilarity search:")

print(
    "Document:",
    results["documents"][0][0]
)

print(
    "Distance:",
    results["distances"][0][0]
)