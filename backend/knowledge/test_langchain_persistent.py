from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DIR = Path(__file__).parent / "test_langchain_persistent"

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
print("LangChain Persistent Chroma Test")
print("=" * 60)


# --------------------------------------------------
# 1. Embedding
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

query_embedding = embeddings.embed_query(TEXT)

print("\nQuery embedding:")
print(query_embedding[:10])

print("Dimension:")
print(len(query_embedding))


# --------------------------------------------------
# 2. Create LangChain Chroma
# --------------------------------------------------

document = Document(
    page_content=TEXT,
    metadata={
        "question": TEXT,
    },
)


vectorstore = Chroma.from_documents(
    documents=[document],
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR),
)


# --------------------------------------------------
# 3. Read stored embedding
# --------------------------------------------------

result = vectorstore.get(
    include=["documents", "embeddings"],
)


stored_embedding = result["embeddings"][0]


print("\nStored embedding:")
print(stored_embedding[:10])

print("\nStored dimension:")
print(len(stored_embedding))


# --------------------------------------------------
# 4. Compare embeddings
# --------------------------------------------------

cosine = cosine_similarity(
    query_embedding,
    stored_embedding,
)

euclidean = euclidean_distance(
    query_embedding,
    stored_embedding,
)


print("\nEmbedding comparison:")
print(f"Cosine similarity: {cosine:.6f}")
print(f"Euclidean distance: {euclidean:.6f}")


# --------------------------------------------------
# 5. Similarity search
# --------------------------------------------------

results = vectorstore.similarity_search_with_score(
    TEXT,
    k=1,
)


print("\nSimilarity search:")

for doc, score in results:
    print(f"Score: {score}")
    print(f"Document: {doc.page_content}")