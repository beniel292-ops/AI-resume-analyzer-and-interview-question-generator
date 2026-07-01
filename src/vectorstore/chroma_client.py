import chromadb
from config.settings import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME
from utils.logger import get_logger

logger = get_logger(__name__)

_client = None
_collection = None


def get_collection():
    """Get (or create) the persistent Chroma collection, cached after first call."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
        _collection = _client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
        logger.info(f"Chroma collection ready: {CHROMA_COLLECTION_NAME}")
    return _collection


def add_chunks(chunks_data: list[dict], embeddings: list[list[float]]):
    """Add chunks and embeddings to the collection with advanced metadata."""
    collection = get_collection()
    
    texts = []
    metadatas = []
    ids = []
    
    for i, data in enumerate(chunks_data):
        texts.append(data["text"])
        meta = data["metadata"]
        metadatas.append(meta)
        ids.append(f"{meta['source']}_page{meta['page']}_chunk{meta['chunk_index']}")
        
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Successfully stored {len(texts)} chunks into ChromaDB.")


def query_similar(query_embedding: list[float], n_results: int = 3) -> dict:
    """
    Find the n_results chunks whose embeddings are closest to query_embedding.
    Returns Chroma's raw result dict — documents, metadatas, distances,
    each as a list of lists (one inner list per query, since Chroma supports
    batched queries — we only ever send one query at a time here).
    """
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results
