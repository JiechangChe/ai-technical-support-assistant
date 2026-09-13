import jieba
from sentence_transformers import CrossEncoder

from knowledge.vectorstore import get_vectorstore


STOPWORDS = {
    "的", "了", "在", "是", "我", "有", "和",
    "就", "不", "人", "都", "一", "一个", "上",
    "也", "很", "到", "说", "要", "去", "你",
    "会", "着", "没有", "看", "好", "自己", "这",
}


RERANKER_MODEL = "BAAI/bge-reranker-base"


def extract_keywords(query: str) -> list[str]:
    words = jieba.lcut(query)

    return [
        word
        for word in words
        if word not in STOPWORDS and len(word) > 1
    ]


def keyword_filter(
    query: str,
    docs: list,
    min_match_ratio: float = 0.3,
) -> list:
    keywords = extract_keywords(query)

    if not keywords:
        return docs

    scored_docs = []

    for doc in docs:
        content = doc.page_content

        match_count = sum(
            1
            for keyword in keywords
            if keyword in content
        )

        ratio = match_count / len(keywords)

        if ratio >= min_match_ratio:
            scored_docs.append(
                (doc, ratio)
            )

    scored_docs.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        doc
        for doc, _ in scored_docs
    ] if scored_docs else docs


def rerank_documents(
    query: str,
    docs: list,
    top_k: int = 3,
) -> list:
    if not docs:
        return []

    reranker = CrossEncoder(
        RERANKER_MODEL,
        max_length=512,
    )

    candidate_docs = docs[:10]

    pairs = [
        [query, doc.page_content]
        for doc in candidate_docs
    ]

    scores = reranker.predict(pairs)

    scored_docs = sorted(
        zip(candidate_docs, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        doc
        for doc, _ in scored_docs[:top_k]
    ]


def retrieve_documents(
    query: str,
    k: int = 30,
    top_k: int = 3,
) -> list:
    vectorstore = get_vectorstore()

    docs = vectorstore.similarity_search(
        query,
        k=k,
    )

    docs = keyword_filter(
        query,
        docs,
    )

    docs = rerank_documents(
        query,
        docs,
        top_k=top_k,
    )

    return docs