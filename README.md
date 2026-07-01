# Local RAG AI Assistant

This repository contains a complete, 100% locally hosted Retrieval-Augmented Generation (RAG) AI application. 
It ensures absolute privacy by running the embedding models, the vector database, and the large language model directly on your local hardware. No data is ever sent to external cloud APIs like OpenAI or Anthropic.

## Architecture Overview

The system is built in three distinct phases:

### Phase 1: Knowledge Ingestion & Embeddings
- **Loaders**: Extracts text from `.txt`, `.pdf`, and `.docx` files. It extracts page-level metadata for traceability.
- **Chunker**: Splits large documents into overlapping 500-character chunks to ensure the LLM receives highly relevant and specific context rather than overwhelming walls of text.
- **Embedder**: Converts text chunks into 384-dimensional numerical vectors using `sentence-transformers/all-MiniLM-L6-v2`. This mathematical representation captures the semantic meaning of the text.

### Phase 2: Vector Storage & Semantic Retrieval
- **Vector Database**: Uses **ChromaDB** running in persistent mode (`chroma.sqlite3`). 
- **Retrieval**: When a user asks a question, the query is embedded using the exact same MiniLM model. ChromaDB performs a mathematical Nearest-Neighbor search (Cosine Distance) to retrieve the top 3 most relevant chunks, completely ignoring exact keyword matches in favor of conceptual similarity.

### Phase 3: Generation (Local LLM)
- **Model Engine**: Uses **Ollama** as the backend inference engine.
- **LLM**: Uses `Qwen2.5-3B-Instruct`. This is a highly optimized, quantized 3 Billion parameter model.
- **Prompt Building**: The retrieved chunks and their metadata are injected into a strict prompt template alongside the user's question, forcing the AI to answer *only* based on the retrieved context.

---

## Repository Structure

```text
rag-ai/
├── data/
│   └── raw/                   # Drop your PDFs, TXTs, and DOCXs here
├── chroma_db/                 # Persistent SQLite Vector Database
├── models/                    # Local cache for the Sentence-Transformer model
├── src/
│   ├── embeddings/            # Embedding generation logic
│   ├── ingestion/             # PDF Loaders and Semantic Chunkers
│   ├── llm/                   # Ollama API Client
│   ├── memory/                # Multi-turn conversation history
│   ├── rag/                   # Core RAG pipeline and Prompt Builder
│   └── vectorstore/           # ChromaDB client and query logic
├── ingest.py                  # Bulk ingestion script for the data/raw folder
├── pdf_ingest.py              # Dedicated script for single PDF ingestion
├── verify_database.py         # Debug tool: View stored chunks and DB metrics
├── verify_retrieval.py        # Debug tool: Bypass LLM to view raw similarity scores
└── app.py                     # The interactive AI chat terminal
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed on your system.

### 2. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Ollama
In a separate terminal, pull the highly optimized quantized model:
```bash
ollama run qwen2.5:3b
```
*(Once downloaded, you can close that terminal, Ollama runs in the background).*

### 4. Ingest Your Documents
Place your knowledge files inside `data/raw/` and run:
```bash
python ingest.py
```
*(Or use `python pdf_ingest.py <path_to_pdf>` for specific files).*

### 5. Chat with your Data
```bash
python app.py
```