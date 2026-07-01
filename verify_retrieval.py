import sys
from src.rag.retriever import retrieve_relevant_chunks
from src.rag.prompt_builder import build_rag_prompt

def verify_retrieval(query: str):
    print("========================================")
    print("        Retrieval Verification          ")
    print("========================================")
    print(f"Query: '{query}'\n")
    
    chunks = retrieve_relevant_chunks(query, n_results=3)
    
    if not chunks:
        print("No chunks retrieved!")
        return
        
    print(f"Retrieved {len(chunks)} chunks.\n")
    
    for idx, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {idx} ---")
        meta = chunk.get("metadata", {})
        
        # Display extracted metadata
        source = meta.get("source", "Unknown")
        page = meta.get("page", "Unknown")
        distance = chunk.get("distance", "N/A")
        
        print(f"Source PDF/File: {source}")
        print(f"Page Number: {page}")
        print(f"Similarity Distance: {distance:.4f} (Lower is more relevant)")
        print(f"Text:\n{chunk['text']}\n")
        
    print("========================================")
    print("   Exact Prompt Sent to LLM (Audit)     ")
    print("========================================")
    prompt = build_rag_prompt(query, chunks, chat_history="")
    print(prompt)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        verify_retrieval(query)
    else:
        q = input("Enter a query to verify retrieval: ")
        verify_retrieval(q)
