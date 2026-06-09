import os
import re
import json
import random

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
CHUNKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chunks.json")

CHUNK_SIZE = 800
OVERLAP = 150


def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;|&amp;|&lt;|&gt;|&quot;', ' ', text)
    text = re.sub(r'\(Image credit:[^)]*\)', '', text)
    text = re.sub(r'Image \d+ of \d+', '', text)
    text = re.sub(r'Latest Videos From.*', '', text)
    text = re.sub(r'Why you can trust Tom\'s Hardware.*?Find out more about how we test\.?', '', text, flags=re.DOTALL)
    text = re.sub(r'Swipe to scroll horizontally', '', text)
    text = re.sub(r'Row \d+ - Cell \d+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            lines.append('')
            continue
        if len(line) < 10:
            continue
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 50]


def load_and_chunk_documents() -> list[dict]:
    all_chunks = []

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith('.txt'):
            continue

        filepath = os.path.join(DOCS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned, CHUNK_SIZE, OVERLAP)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": filename,
                "chunk_index": i,
            })

    return all_chunks


def save_chunks(chunks: list[dict]) -> None:
    with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def load_chunks() -> list[dict]:
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    save_chunks(chunks)

    print(f"Total chunks: {len(chunks)}")
    print(f"Documents processed: {len(set(c['source'] for c in chunks))}")
    print()

    sample = random.sample(chunks, min(5, len(chunks)))
    for i, chunk in enumerate(sample, 1):
        print(f"--- Sample Chunk {i} [source: {chunk['source']}, index: {chunk['chunk_index']}] ---")
        print(chunk["text"][:300])
        print("...")
        print()
