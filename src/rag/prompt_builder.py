def build_rag_prompt(query: str, retrieved_chunks: list[dict], chat_history: str = "", system_context: str = "") -> str:
    """
    Constructs the final prompt string that gets fed to the LLM.
    It combines the chat history (if any), the retrieved chunks, the system context (if any), and the user's query.
    """
    if system_context:
        prompt = f"System Context:\n{system_context}\n\n"
        prompt += "Use the System Context and the following retrieved context to answer the question at the end.\n"
    else:
        prompt = "Use the following context to answer the question at the end.\n"
        prompt += "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
    
    if chat_history:
        prompt += f"--- Chat History ---\n{chat_history}\n\n"
        
    prompt += "--- Retrieved Context ---\n"
    for idx, chunk in enumerate(retrieved_chunks, start=1):
        prompt += f"Chunk {idx} (Source: {chunk['source']}):\n{chunk['text']}\n\n"
        
    prompt += f"--- Question ---\n{query}\n"
    return prompt
