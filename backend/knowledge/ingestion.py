from pathlib import Path

from knowledge.loader import (
    load_knowledge_documents,
    split_documents,
)

from knowledge.vectorstore import (
    embed_text,
    get_chroma_collection,
)


KNOWLEDGE_FILE = (
    Path(__file__).parent
    / "data"
    / "副本技术支持AI问题库.xlsx"
)


def build_vectorstore():
    print("Loading knowledge base...")

    documents = load_knowledge_documents(
        str(KNOWLEDGE_FILE)
    )

    print(
        f"Loaded documents: {len(documents)}"
    )

    chunks = split_documents(documents)

    print(
        f"Created chunks: {len(chunks)}"
    )

    collection = get_chroma_collection()

    # Clear existing data
    existing = collection.get()

    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )

    print("\nGenerating embeddings...")

    ids = []
    texts = []
    embeddings = []
    metadatas = []

    for index, document in enumerate(chunks):

        text = document.page_content

        embedding = embed_text(text)

        ids.append(
            f"knowledge-{index}"
        )

        texts.append(text)

        embeddings.append(
            embedding
        )

        metadatas.append(
            document.metadata
        )

    print(
        f"Generated embeddings: {len(embeddings)}"
    )

    print("\nWriting to Chroma...")

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Chroma document count: "
        f"{collection.count()}"
    )

    print(
        f"Chroma database created at: "
        f"{Path(__file__).parent / 'chroma_db'}"
    )


if __name__ == "__main__":
    build_vectorstore()