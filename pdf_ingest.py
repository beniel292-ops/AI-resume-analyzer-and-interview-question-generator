import sys
from pathlib import Path
from src.ingestion.loaders import load_pdf
from src.ingestion.chunker import chunk_document
from src.embeddings.embedder import embed_texts
from src.vectorstore.chroma_client import get_collection, add_chunks
from utils.logger import get_logger

logger = get_logger(__name__)

def ingest_pdf(pdf_path_str: str):
    file_path = Path(pdf_path_str)
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return
        
    if file_path.suffix.lower() != ".pdf":
        logger.error("This script is specifically for PDF files.")
        return
        
    # Check for duplicates
    collection = get_collection()
    existing = collection.get(where={"source": file_path.name}, limit=1)
    if existing["ids"]:
        logger.error(f"PDF {file_path.name} has already been ingested into the database! Skipping to prevent duplicates.")
        return

    logger.info(f"Starting ingestion for {file_path.name}...")
    
    pages_data = load_pdf(file_path)
    if not pages_data:
        logger.warning("No text could be extracted.")
        return
        
    chunks_data = chunk_document(pages_data)
    texts = [c["text"] for c in chunks_data]
    
    logger.info(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = embed_texts(texts)
    
    logger.info("Storing in ChromaDB...")
    add_chunks(chunks_data, embeddings)
    logger.info("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_ingest.py <path_to_pdf>")
    else:
        ingest_pdf(sys.argv[1])
