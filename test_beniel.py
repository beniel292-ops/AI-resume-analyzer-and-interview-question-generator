import sys
from src.rag.pipeline import ask_rag_assistant
from src.llm.qwen_client import get_llm

def test_generation():
    query = "What are Beniel's skills and what projects did he build?"
    print(f"Query: {query}")
    
    # Pre-load to avoid noisy logs during generation
    get_llm()
    
    print("\n--- Generating Response ---")
    response = ask_rag_assistant(query)
    print("\n--- Final Output ---")
    print(response)

if __name__ == "__main__":
    test_generation()
