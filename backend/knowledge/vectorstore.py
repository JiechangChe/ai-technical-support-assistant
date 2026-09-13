from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DIR = Path(__file__).parent / "chroma_db"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


def get_vectorstore():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )