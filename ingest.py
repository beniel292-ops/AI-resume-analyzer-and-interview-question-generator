from pathlib import Path
from config.settings import DATA_RAW_DIR
from src.ingestion.loaders import load_document
from src.ingestion.chunker import chunk_document
from src.embeddings.embedder import embed_texts
from src.vectorstore.chroma_client import add_chunks
from utils.logger import get_logger

logger = get_logger(__name__)


def ingest_file(file_path: Path):
    pages_data = load_document(file_path)
    if not pages_data:
        logger.warning(f"No text extracted from {file_path.name}, skipping.")
        return
        
    chunks_data = chunk_document(pages_data)
    texts_only = [c["text"] for c in chunks_data]
    
    embeddings = embed_texts(texts_only)
    add_chunks(chunks_data, embeddings)
    logger.info(f"Ingestion complete for {file_path.name}: {len(chunks_data)} chunks stored")


def main():
    supported_extensions = ["*.txt", "*.pdf", "*.docx"]
    files_to_ingest = []
    
    for ext in supported_extensions:
        files_to_ingest.extend(DATA_RAW_DIR.glob(ext))
        
    if not files_to_ingest:
        logger.warning(f"No supported documents found in {DATA_RAW_DIR}")
        return

    for file_path in files_to_ingest:
        ingest_file(file_path)


if __name__ == "__main__":
    main()
