from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

text = "新创建的仓库为什么看不到库存"


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


print("=" * 60)
print("Embedding Implementation Comparison")
print("=" * 60)


# --------------------------------------------------
# 1. SentenceTransformer
# --------------------------------------------------

sentence_model = SentenceTransformer(MODEL_NAME)

sentence_embedding = sentence_model.encode(text)


# --------------------------------------------------
# 2. LangChain HuggingFaceEmbeddings
# --------------------------------------------------

langchain_embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

langchain_embedding = (
    langchain_embeddings.embed_query(text)
)


# --------------------------------------------------
# 3. Compare
# --------------------------------------------------

print("\nSentenceTransformer:")
print(sentence_embedding[:10])

print("\nLangChain HuggingFaceEmbeddings:")
print(langchain_embedding[:10])

print("\nDimensions:")
print("SentenceTransformer:", len(sentence_embedding))
print("LangChain:", len(langchain_embedding))

print("\nCosine similarity:")
print(
    cosine_similarity(
        sentence_embedding,
        langchain_embedding,
    )
)

print("\nEuclidean distance:")
print(
    np.linalg.norm(
        sentence_embedding - langchain_embedding
    )
)