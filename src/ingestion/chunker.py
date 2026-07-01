import time
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_document(pages: list[dict], chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """
    Split text into overlapping chunks while preserving metadata.
    
    Why chunking is needed:
    LLMs have a maximum context window. We cannot feed an entire 100-page PDF into Qwen at once.
    Even if we could, finding the *exact* answer is harder if the context is flooded with irrelevant pages.
    By breaking docs into 500-character chunks, we only retrieve the highly relevant snippets.
    
    Recommended chunk size: 500-1000 characters.
    Recommended overlap: 10-20% (e.g. 50-100 characters) to prevent cutting sentences in half.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    all_chunks = []
    
    for page_data in pages:
        text = page_data["text"]
        base_meta = page_data["metadata"]
        
        start = 0
        text_length = len(text)
        
        chunk_idx = 0
        while start < text_length:
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Create a new metadata dict for this specific chunk
            chunk_meta = base_meta.copy()
            chunk_meta["chunk_index"] = chunk_idx
            chunk_meta["ingestion_timestamp"] = int(time.time())
            
            all_chunks.append({
                "text": chunk_text,
                "metadata": chunk_meta
            })
            
            start += (chunk_size - overlap)
            chunk_idx += 1
            
    return all_chunks
