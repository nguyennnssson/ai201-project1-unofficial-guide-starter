# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Laptop reviews from major tech publications. This knowledge is valuable because buying a laptop is a significant investment, and prospective buyers need consolidated, honest assessments that go beyond manufacturer marketing. While individual reviews exist across many sites, there is no single place to query across multiple publications and get a synthesized, source-cited answer about a specific laptop's strengths, weaknesses, or how it compares to alternatives. This system lets users ask natural-language questions and get grounded answers drawn from real expert reviews.

---

## Documents

12 laptop reviews from Tom's Hardware and Laptop Mag covering a range of laptop categories (gaming, ultraportable, productivity, budget) across 8 brands and price ranges from $800 to $3,299.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Tom's Hardware | Asus ROG Strix Scar 16 (2025) RTX 5080 gaming laptop review | https://www.tomshardware.com/laptops/gaming-laptops/asus-rog-strix-scar-16-2025-rtx-5080-gaming-laptop-review |
| 2 | Tom's Hardware | Gigabyte G6X gaming laptop review | https://www.tomshardware.com/laptops/gaming-laptops/gigabyte-g6x-gaming-laptop-review |
| 3 | Tom's Hardware | MSI Katana 17 HX gaming laptop review | https://www.tomshardware.com/laptops/gaming-laptops/msi-katana-17-hx-gaming-laptop-review |
| 4 | Tom's Hardware | Dell G15 (5520) gaming laptop review | https://www.tomshardware.com/reviews/dell-g15-5520 |
| 5 | Tom's Hardware | HP Spectre x360 13-inch laptop review | https://www.tomshardware.com/reviews/hp-spectre-x360-13-inch-laptop,6083.html |
| 6 | Tom's Hardware | HP Omen X 2S 15 gaming laptop review | https://www.tomshardware.com/reviews/hp-omen-x-2s-15-gaming-laptop,6261.html |
| 7 | Laptop Mag | MacBook Air 15-inch (M3) review | https://www.laptopmag.com/laptops/macbooks/macbook-air-15-inch-m3 |
| 8 | Laptop Mag | Dell XPS 14 (2024) review | https://www.laptopmag.com/laptops/dell-xps-14-2024 |
| 9 | Laptop Mag | Lenovo Legion Pro 5i (Gen 8) review | https://www.laptopmag.com/reviews/lenovo-legion-pro-5i-review-subtle-styling-performance-and-price-tag-make-this-a-win |
| 10 | Laptop Mag | HP Victus 15 (2022) review | https://www.laptopmag.com/reviews/hp-victus-15-2022-review-is-this-dollar800-gaming-laptop-actually-good |
| 11 | Laptop Mag | Microsoft Surface Pro (11th Edition) review | https://www.laptopmag.com/reviews/microsoft-surface-pro-11th-edition |
| 12 | Laptop Mag | Lenovo Yoga Slim 7x review | https://www.laptopmag.com/laptops/lenovo-yoga-slim-7x |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Reasoning:**
These documents are medium-to-long form reviews (600–3,700 words each) with multiple sections covering specs, design, display, performance, battery, keyboard, pros/cons, and verdicts. An 800-character chunk captures roughly one complete section or topic (e.g., an entire display assessment or battery life discussion), which is ideal for semantic retrieval — each chunk carries enough context to be meaningful on its own.

The 150-character overlap ensures that facts spanning section boundaries are captured in at least one chunk. For example, if a verdict references a display score mentioned at the end of the previous section, the overlap preserves that connection.

If chunks were too small (e.g., 300 chars), individual benchmark numbers or specs would be isolated from their context, making retrieval less useful. If chunks were too large (e.g., 1500+ chars), retrieval would return diluted context mixing unrelated topics (e.g., battery life details mixed with keyboard assessment), reducing answer precision.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 (sentence-transformers). This is a lightweight, local model that produces 384-dimensional embeddings. It runs without an API key and has no rate limits, making it ideal for development.

**Top-k:** k=5. With 12 documents producing ~209 total chunks, k=5 retrieves roughly 2.4% of the corpus. This is enough to capture relevant information from 2–3 different reviews when a question mentions a specific laptop, while keeping the LLM context focused. k=3 risks missing relevant information when multiple reviews contain complementary details. k=10 would dilute the context with marginally relevant chunks and risk the LLM averaging over noise.

**Production tradeoff reflection:**
For production, I would weigh these factors when selecting an embedding model:
- **Cost:** all-MiniLM-L6-v2 is free and runs locally, but API-based models (OpenAI text-embedding-3-small, Cohere embed-v3) charge per token and add latency. For a small corpus like this, local is clearly better.
- **Context length:** all-MiniLM-L6-v2 accepts up to 256 tokens, which fits our 800-character chunks. Longer documents or larger chunks would need a model with a bigger context window like nomic-embed-text (8192 tokens).
- **Multilingual support:** This model is English-focused. For a multilingual review corpus, paraphrase-multilingual-MiniLM-L12-v2 would be needed.
- **Quality vs. speed:** Larger models like all-mpnet-base-v2 (768 dimensions) produce better embeddings but take 2x longer to encode and require more storage. For 209 chunks the speed difference is negligible, but at scale it matters.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the battery life of the MacBook Air 15 M3? | 15 hours and 3 minutes on continuous web surfing at 150 nits |
| 2 | What GPU does the Dell XPS 14 2024 use and how does it perform in games? | Nvidia GeForce RTX 4050 with 6GB VRAM; Shadow of the Tomb Raider at 50 fps, Civilization VI at 88 fps at 1080p |
| 3 | What are the main cons of the Microsoft Surface Pro 11th Edition? | Shallow keyboard, poor trackpad, limited ports, expensive for tablet functionality |
| 4 | How does the HP Victus 15 compare to the Acer Nitro 5 for budget gaming? | The Victus 15 is thinner/lighter but has a weaker GPU (GTX 1650 vs RTX 30-series), worse battery, and the Nitro 5 offers better value |
| 5 | What is the display brightness of the Lenovo Yoga Slim 7x in SDR mode? | 464 nits average in SDR, with peak HDR brightness of 785 nits |

---

## Anticipated Challenges

1. **Chunk boundary splits on key facts:** Specific numbers like battery life hours or benchmark scores may land at the boundary between two chunks, so neither chunk alone contains the complete fact. The 150-character overlap mitigates this but won't catch every case — especially when a heading and its value are separated by more than 150 characters.

2. **Cross-review contamination in retrieval:** When a user asks about a specific laptop, the retriever might pull chunks from similarly-named or similarly-specced laptops (e.g., "Dell G15" vs "Dell XPS 14"). Source metadata labeling in the prompt should help the LLM distinguish, but the model may still blend information from multiple sources into a single claim.

3. **Grounding enforcement against training data:** The LLM may try to answer from its training data for well-known products like the MacBook Air. The system prompt must strictly enforce answering only from retrieved context, and we need to test with out-of-scope queries to verify.

4. **Scraping noise in Tom's Hardware content:** Some scraped content includes image credits, navigation fragments, and boilerplate text that survived cleaning. The ingestion pipeline needs robust regex-based cleaning to strip these artifacts.

---

## Architecture

```
documents/ (12 .txt files)
    |
    v
[ingest.py] -- Load -> Clean -> Chunk (800 chars, 150 overlap)
    |
    v
[embed.py] -- all-MiniLM-L6-v2 -> ChromaDB (PersistentClient)
    |
    v
[retrieve.py] -- User query -> Embed -> Cosine similarity -> Top-5 chunks
    |
    v
[query.py] -- Chunks + System prompt -> Groq API (llama-3.3-70b-versatile) -> Grounded answer + sources
    |
    v
[app.py] -- Gradio web UI (question input -> answer + sources output)
    |
    v
[evaluate.py] -- 5 test questions -> Compare expected vs. actual -> Report
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
I will give Claude my Chunking Strategy section from this planning.md and ask it to implement `ingest.py` with `clean_text()` and `chunk_text()` functions using my specified 800-character chunk size and 150-character overlap. I will also provide it with sample raw document text so it can write appropriate cleaning regexes for Tom's Hardware boilerplate (image credits, navigation text). I will verify the output by running the script and printing 5 random chunks to check they are readable, substantive, and free of HTML artifacts.

**Milestone 4 — Embedding and retrieval:**
I will ask Claude to implement `embed.py` using sentence-transformers with all-MiniLM-L6-v2 and ChromaDB PersistentClient, and `retrieve.py` with a `retrieve(query, k=5)` function. I will verify by running 3 of my evaluation queries and checking that the returned chunks are from the correct source documents with distance scores below 0.9.

**Milestone 5 — Generation and interface:**
I will give Claude my grounding system prompt and ask it to implement `query.py` with the Groq API (llama-3.3-70b-versatile) and `app.py` with a Gradio interface. I will verify grounding by testing an out-of-scope query (e.g., "What is the price of the iPhone 16 Pro?") and confirming the system refuses to answer from training data.
