from config.settings import EMBEDDING_MODEL_NAME
from sentence_transformers import SentenceTransformer
from utils.logger import get_logger

logger = get_logger(__name__)

_model = None  # module-level cache — loaded once, reused everywhere


def get_embedder() -> SentenceTransformer:
    """
    Load the embedding model once and reuse it.
    Loading a model is expensive (reads weights from disk into memory);
    doing it on every function call would make ingestion painfully slow.
    """
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert a list of text chunks into a list of embedding vectors."""
    model = get_embedder()
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()
