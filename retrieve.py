from sentence_transformers import SentenceTransformer
import chromadb
import os

CHROMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "laptop_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = 5) -> list[dict]:
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta["source"], "distance": dist})
    return chunks


if __name__ == "__main__":
    test_queries = [
        "What is the battery life of the MacBook Air 15 M3?",
        "What GPU does the Dell XPS 14 use?",
        "What are the cons of the Microsoft Surface Pro 11?",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        results = retrieve(q)
        for i, r in enumerate(results):
            print(f"  [{i+1}] dist={r['distance']:.3f} | source={r['source']}")
            print(f"      {r['text'][:150]}...")
        print()
