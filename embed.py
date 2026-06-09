from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_chunks, CHUNKS_FILE
import os

CHROMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "laptop_reviews"


def embed_chunks():
    if not os.path.exists(CHUNKS_FILE):
        print("No chunks.json found. Run ingest.py first.")
        return

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() > 0:
        print(f"Collection already has {collection.count()} items. Skipping embedding.")
        print("Delete chroma_db/ directory to re-embed.")
        return

    chunks = load_chunks()
    print(f"Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts).tolist()

        ids = [f"{c['source']}_{c['chunk_index']}" for c in batch]
        metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in batch]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        print(f"  Embedded {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

    print(f"Done. {collection.count()} chunks embedded into ChromaDB.")


if __name__ == "__main__":
    embed_chunks()
