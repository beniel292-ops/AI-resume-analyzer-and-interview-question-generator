from src.rag.retriever import retrieve_relevant_chunks
from src.rag.prompt_builder import build_rag_prompt
from src.llm.qwen_client import generate_answer
from utils.logger import get_logger

logger = get_logger(__name__)

def ask_rag_assistant(query: str, chat_history: str = "") -> str:
    """
    The full RAG pipeline:
    1. Retrieve relevant chunks
    2. Build prompt with chunks and history
    3. Generate answer
    """
    logger.info(f"Starting RAG pipeline for query: '{query}'")
    
    # 1. Retrieve
    chunks = retrieve_relevant_chunks(query, n_results=3)
    if not chunks:
        return "I don't have any relevant information in my database to answer this."
        
    # 2. Build Prompt
    prompt = build_rag_prompt(query, chunks, chat_history)
    
    # 3. Generate Answer
    answer = generate_answer(prompt)
    logger.info("RAG pipeline complete.")
    
    return answer
