# Load the resource excel as document, split it into chunks, embedding, save in the Chromadb
# for constructing Construct the knowledge base
from pathlib import Path

from langchain_community.vectorstores import Chroma

from knowledge.loader import (
    load_knowledge_documents,
    split_documents,
)

from knowledge.vectorstore import (
    CHROMA_DIR,
    get_embeddings,
)


KNOWLEDGE_FILE = (
    Path(__file__).parent
    / "data"
    / "副本技术支持AI问题库.xlsx"
)



def build_vectorstore():
    print("Loading knowledge base...")

    # Load document
    documents = load_knowledge_documents(
        str(KNOWLEDGE_FILE)
    )

    print(f"Loaded documents: {len(documents)}")

    # Split document into chunks
    chunks = split_documents(documents)

    print(f"Created chunks: {len(chunks)}")

    embeddings = get_embeddings()

    print("Creating Chroma vector store...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"Chroma database created at: {CHROMA_DIR}")


if __name__ == "__main__":
    build_vectorstore()