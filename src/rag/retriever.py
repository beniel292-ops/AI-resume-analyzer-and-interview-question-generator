from src.embeddings.embedder import embed_texts
from src.vectorstore.chroma_client import query_similar
from utils.logger import get_logger

logger = get_logger(__name__)


def retrieve_relevant_chunks(query: str, n_results: int = 3) -> list[dict]:
    """
    Full retrieval step: embed the query, search Chroma, return a clean
    list of {text, source, chunk_index, distance} dicts — one per match,
    ranked from most to least relevant (lowest distance first).
    """
    query_embedding = embed_texts([query])[0]  # embed_texts expects a list, we send one query
    raw_results = query_similar(query_embedding, n_results=n_results)

    chunks = []
    documents = raw_results["documents"][0]      # unwrap the outer "per-query" list
    metadatas = raw_results["metadatas"][0]
    distances = raw_results["distances"][0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        chunks.append({
            "text": doc,
            "source": meta.get("source"),
            "chunk_index": meta.get("chunk_index"),
            "distance": dist,
        })

    logger.info(f"Retrieved {len(chunks)} chunks for query: '{query}'")
    return chunks
