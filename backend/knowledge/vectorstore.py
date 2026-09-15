from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DIR = Path(__file__).parent / "chroma_db"

COLLECTION_NAME = "technical_support"


_embedding_model = None
_chroma_client = None
_collection = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _embedding_model


def get_chroma_collection():
    global _chroma_client
    global _collection

    if _collection is None:
        _chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    return _collection


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()

    return model.encode(text).tolist()