import hashlib
import os
import sys
from pathlib import Path
from utils.logger import get_logger

project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from src.ingestion.loaders import load_pdf
from src.ingestion.chunker import chunk_document
from src.embeddings.embedder import embed_texts
from src.vectorstore.chroma_client import get_collection, add_chunks
from src.resume.analyzer import extract_resume
from src.questions.generator import generate_questions

logger = get_logger(__name__)

def simulate_upload(pdf_path: Path):
    logger.info(f"Simulating upload of {pdf_path.name}")
    bytes_data = pdf_path.read_bytes()
    file_hash = hashlib.sha256(bytes_data).hexdigest()
    
    collection = get_collection()
    existing = collection.get(where={"file_hash": file_hash}, limit=1)
    
    pages_data = load_pdf(pdf_path)
    
    if existing and existing.get("ids"):
        logger.info("Duplicate check passed: PDF already ingested in ChromaDB.")
    else:
        logger.info("New file detected. Ingesting into ChromaDB...")
        for page in pages_data:
            page["metadata"]["file_hash"] = file_hash
            page["metadata"]["source"] = pdf_path.name
            
        chunks_data = chunk_document(pages_data)
        if chunks_data:
            texts = [c["text"] for c in chunks_data]
            embeddings = embed_texts(texts)
            add_chunks(chunks_data, embeddings)
            logger.info("Successfully chunked and stored in ChromaDB.")
            
    # Combine text
    full_text = "\n".join([page["text"] for page in pages_data])
    
    logger.info("Running Resume Analyzer...")
    resume_data = extract_resume(full_text)
    logger.info("Extracted Name: " + resume_data.name)
    
    logger.info("Generating Interview Questions...")
    questions = generate_questions(resume_data)
    logger.info(f"Generated {len(questions.questions)} questions.")
    
    return True

if __name__ == "__main__":
    test_pdf = Path("sample_resume.pdf")
    logger.info("--- RUN 1 (Should Ingest) ---")
    simulate_upload(test_pdf)
    
    logger.info("--- RUN 2 (Should Skip Ingest) ---")
    simulate_upload(test_pdf)
    
    logger.info("Phase 5 simulation successful!")
