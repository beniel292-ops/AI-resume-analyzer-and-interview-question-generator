import chromadb
from config.settings import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME
import json

def verify_db():
    print("========================================")
    print("        ChromaDB Verification           ")
    print("========================================")
    print(f"Database Path: {CHROMA_DB_DIR}")
    
    # 1. Connect to Persistent Client
    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
        print("[OK] Connected to PersistentClient (Disk Storage)")
    except Exception as e:
        print(f"[FAIL] Could not connect to ChromaDB: {e}")
        return

    # 2. List Collections
    collections = client.list_collections()
    print(f"\nTotal Collections Found: {len(collections)}")
    for c in collections:
        print(f" - {c.name}")
        
    # 3. Inspect target collection
    try:
        collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
    except Exception:
        print(f"\n[WARN] Collection '{CHROMA_COLLECTION_NAME}' does not exist yet.")
        print("Run ingest.py or pdf_ingest.py to populate it.")
        return
        
    count = collection.count()
    print(f"\n--- Metrics for '{CHROMA_COLLECTION_NAME}' ---")
    print(f"Total Stored Documents (Chunks): {count}")
    
    # 4. Display Sample
    if count > 0:
        print("\n--- Sample Document (First Item) ---")
        results = collection.get(limit=1, include=["documents", "metadatas", "embeddings"])
        
        doc_id = results['ids'][0]
        doc_text = results['documents'][0]
        doc_meta = results['metadatas'][0]
        
        # Verify embeddings exist without printing huge arrays
        has_embedding = results['embeddings'] is not None and len(results['embeddings']) > 0
        embedding_len = len(results['embeddings'][0]) if has_embedding else 0
        
        print(f"Document ID: {doc_id}")
        print(f"Metadata: {json.dumps(doc_meta, indent=2)}")
        print(f"Embedding Present: {'Yes' if has_embedding else 'No'} (Dimensions: {embedding_len})")
        print(f"Text Snippet: {doc_text[:200]}...")
        
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_db()
