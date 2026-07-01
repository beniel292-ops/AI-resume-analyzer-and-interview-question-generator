from config.settings import EMBEDDING_MODEL_NAME, LLM_MODEL_NAME
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info(f"Starting download of embedding model: {EMBEDDING_MODEL_NAME}")
    SentenceTransformer(EMBEDDING_MODEL_NAME)
    logger.info("Embedding model downloaded successfully.")

    logger.info(f"Starting download of LLM model: {LLM_MODEL_NAME} (this may take a while...)")
    AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
    AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, device_map="auto")
    logger.info("LLM model downloaded successfully.")

if __name__ == "__main__":
    main()
