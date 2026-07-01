import sys
from src.rag.retriever import retrieve_relevant_chunks


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Ask something about your notes: ")
    results = retrieve_relevant_chunks(query, n_results=3)

    print(f"\nTop {len(results)} results for: '{query}'\n")
    for i, r in enumerate(results, start=1):
        print(f"--- Result {i} (distance: {r['distance']:.4f}, source: {r['source']}) ---")
        print(r["text"])
        print()


if __name__ == "__main__":
    main()
