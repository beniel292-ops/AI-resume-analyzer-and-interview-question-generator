from pathlib import Path
import os

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
MODELS_DIR = BASE_DIR / "models"

# Force huggingface to use the local models folder instead of ~/.cache
os.environ["HF_HOME"] = str(MODELS_DIR)

# --- Chunking ---
CHUNK_SIZE = 500        # characters per chunk
CHUNK_OVERLAP = 50      # characters shared between consecutive chunks

# --- Embedding model ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# --- ChromaDB ---
CHROMA_COLLECTION_NAME = "personal_knowledge_v2"

# --- LLM model ---
LLM_MODEL_NAME = "qwen2.5:3b"

