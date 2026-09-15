import jieba
from sentence_transformers import CrossEncoder

from knowledge.vectorstore import (
    embed_text,
    get_chroma_collection,
)


STOPWORDS = {
    "的", "了", "在", "是", "我", "有", "和",
    "就", "不", "人", "都", "一", "一个", "上",
    "也", "很", "到", "说", "要", "去", "你",
    "会", "着", "没有", "看", "好", "自己", "这",
    "为什么", "怎么", "如何", "可以", "吗",
}


RERANKER_MODEL = "BAAI/bge-reranker-base"

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder(
            RERANKER_MODEL,
            max_length=512,
        )

    return _reranker


def extract_keywords(query: str) -> list[str]:
    words = jieba.lcut(query)

    return [
        word
        for word in words
        if word not in STOPWORDS
        and len(word) > 1
    ]


def keyword_search(query: str, top_k: int = 30) -> list:
    collection = get_chroma_collection()

    results = collection.get(
        include=["documents", "metadatas"]
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    keywords = extract_keywords(query)

    if not keywords:
        return []

    scored_docs = []

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        question = metadata.get("question", "")
        doc_keywords = metadata.get("keywords", "")

        search_text = f"{question} {doc_keywords}"

        match_count = sum(
            1
            for keyword in keywords
            if keyword in search_text
        )

        if match_count > 0:
            scored_docs.append(
                (
                    document,
                    metadata,
                    match_count,
                )
            )

    scored_docs.sort(
        key=lambda x: x[2],
        reverse=True,
    )

    return [
        {
            "document": document,
            "metadata": metadata,
            "keyword_score": score,
        }
        for document, metadata, score in scored_docs[:top_k]
    ]


def vector_search(query: str, k: int = 30) -> list:
    collection = get_chroma_collection()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    docs = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        docs.append(
            {
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return docs


def merge_candidates(
    vector_docs: list,
    keyword_docs: list,
) -> list:

    merged = {}

    for doc in vector_docs:
        question = doc["metadata"].get(
            "question",
            "",
        )

        merged[question] = doc

    for doc in keyword_docs:
        question = doc["metadata"].get(
            "question",
            "",
        )

        if question in merged:
            merged[question].update(doc)
        else:
            merged[question] = doc

    return list(merged.values())


def rerank_documents(
    query: str,
    docs: list,
    top_k: int = 3,
) -> list:

    if not docs:
        return []

    reranker = get_reranker()

    # Rerank the complete candidate set.
    # The current knowledge base is small (~121 documents),
    # so there is no need to truncate to the first 20.
    candidate_docs = docs

    pairs = [
        [query, doc["document"]]
        for doc in candidate_docs
    ]

    scores = reranker.predict(pairs)

    scored_docs = sorted(
        zip(candidate_docs, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        {
            "document": doc["document"],
            "metadata": doc["metadata"],
            "score": float(score),
        }
        for doc, score in scored_docs[:top_k]
    ]


def retrieve_documents(
    query: str,
    k: int = 30,
    top_k: int = 3,
) -> list:

    vector_docs = vector_search(
        query,
        k=k,
    )

    keyword_docs = keyword_search(
        query,
        top_k=k,
    )

    candidates = merge_candidates(
        vector_docs,
        keyword_docs,
    )

    return rerank_documents(
        query,
        candidates,
        top_k=top_k,
    )