import os
from groq import Groq
from retrieve import retrieve
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful laptop review assistant. Answer the user's question using ONLY the information provided in the context below. Do not use your general training knowledge.

If the provided context does not contain enough information to answer, respond with:
'I don't have enough information on that based on the available documents.'

Always cite which document(s) your answer draws from by mentioning the source filename."""


def ask(question: str, k: int = 5) -> dict:
    chunks = retrieve(question, k=k)
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    answer = response.choices[0].message.content
    best_dist = chunks[0]["distance"] if chunks else 1.0
    threshold = best_dist + 0.15
    relevant = [c for c in chunks if c["distance"] <= threshold]
    sources = list(dict.fromkeys(c["source"] for c in relevant))
    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    test = ask("What is the battery life of the MacBook Air 15 M3?")
    print(f"Answer: {test['answer']}")
    print(f"Sources: {test['sources']}")
