# The Unofficial Guide — Project 1

---

## Domain

**Laptop reviews from major tech publications.** Buying a laptop is a significant investment, and prospective buyers need consolidated, honest assessments that go beyond manufacturer marketing. While individual reviews exist across many sites, there is no single place to query across multiple publications and get a synthesized, source-cited answer. This system lets users ask natural-language questions and get grounded answers drawn from 12 real expert reviews spanning gaming laptops, ultraportables, and productivity machines across 8 brands and multiple price ranges ($800–$3,299).

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Asus ROG Strix Scar 16 (2025) RTX 5080 | Tom's Hardware review | https://www.tomshardware.com/laptops/gaming-laptops/asus-rog-strix-scar-16-2025-rtx-5080-gaming-laptop-review |
| 2 | Gigabyte G6X | Tom's Hardware review | https://www.tomshardware.com/laptops/gaming-laptops/gigabyte-g6x-gaming-laptop-review |
| 3 | MSI Katana 17 HX | Tom's Hardware review | https://www.tomshardware.com/laptops/gaming-laptops/msi-katana-17-hx-gaming-laptop-review |
| 4 | Dell G15 (5520) | Tom's Hardware review | https://www.tomshardware.com/reviews/dell-g15-5520 |
| 5 | HP Spectre x360 13 | Tom's Hardware review | https://www.tomshardware.com/reviews/hp-spectre-x360-13-inch-laptop,6083.html |
| 6 | HP Omen X 2S 15 | Tom's Hardware review | https://www.tomshardware.com/reviews/hp-omen-x-2s-15-gaming-laptop,6261.html |
| 7 | MacBook Air 15 M3 (2024) | Laptop Mag review | https://www.laptopmag.com/laptops/macbooks/macbook-air-15-inch-m3 |
| 8 | Dell XPS 14 (2024) | Laptop Mag review | https://www.laptopmag.com/laptops/dell-xps-14-2024 |
| 9 | Lenovo Legion Pro 5i (Gen 8) | Laptop Mag review | https://www.laptopmag.com/reviews/lenovo-legion-pro-5i-review-subtle-styling-performance-and-price-tag-make-this-a-win |
| 10 | HP Victus 15 (2022) | Laptop Mag review | https://www.laptopmag.com/reviews/hp-victus-15-2022-review-is-this-dollar800-gaming-laptop-actually-good |
| 11 | Microsoft Surface Pro 11th Edition | Laptop Mag review | https://www.laptopmag.com/reviews/microsoft-surface-pro-11th-edition |
| 12 | Lenovo Yoga Slim 7x | Laptop Mag review | https://www.laptopmag.com/laptops/lenovo-yoga-slim-7x |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 150 characters

**Why these choices fit your documents:**
These documents are medium-to-long form reviews (600–3,700 words) with distinct sections covering specs, design, display, performance, battery, keyboard, pros/cons, and verdicts. An 800-character chunk captures roughly one complete section or topic, providing enough semantic context for meaningful retrieval. The 150-character overlap ensures facts spanning section boundaries are captured in at least one chunk. Smaller chunks (300 chars) would isolate benchmark numbers from their context. Larger chunks (1500+ chars) would dilute retrieval by mixing unrelated topics like battery life with keyboard quality.

**Final chunk count:** 209 chunks across 12 documents

### Sample Chunks

**Chunk 1** — [source: `macbook_air_15_m3.txt`, index: 5]
```
web surfing at 150 nits. This is a modest 4-minute increase over the M2 model. It significantly
outpaced competitors: the MSI Prestige 16 AI Evo lasted 13 hours 4 minutes, and the Acer Swift
Edge 16 managed only 7 hours 18 minutes. Charging options include a 70W USB-C fast charger or a
dual USB-C 35W adapter that includes a secondary port for other devices.
```

**Chunk 2** — [source: `dell_xps_14_2024.txt`, index: 3]
```
The Intel Core Ultra 7 processor delivers exceptional results. On Geekbench 6.2, the XPS 14
scored 12,711 points, dominating the category average of 8,132. Video transcoding completed in
5:44 on HandBrake, significantly faster than the 8:01 average. Storage transfer rates reached
1,503 MBps.
```

**Chunk 3** — [source: `hp_victus_15.txt`, index: 6]
```
The three-year-old GTX 1650 struggles with demanding titles: Assassin's Creed Valhalla (Very
High): 27 fps (vs. 42.4 fps average), Metro: Exodus (Very High): 26 fps (vs. 39 fps average),
Red Dead Redemption 2 (Very High): 23 fps (vs. 38 fps average)
```

**Chunk 4** — [source: `surface_pro_11.txt`, index: 0]
```
Title: Microsoft Surface Pro (11th Edition) Review: Great, but is it $1,949 great? Source:
https://www.laptopmag.com/reviews/microsoft-surface-pro-11th-edition Specifications: Processor:
Snapdragon X Elite X1E-80-100, RAM: 16GB, Storage: 512GB SSD, Display: 13-inch OLED, 2,880 x
1,920p, 120Hz
```

**Chunk 5** — [source: `lenovo_legion_pro_5.txt`, index: 3]
```
Geekbench 6: 13,634 (exceeds 7,602 average significantly), Assassin's Creed Valhalla (1080p):
103 fps, Red Dead Redemption 2 (1080p): 70 fps, Borderlands 3 (1080p): 90 fps, GTA V (1080p,
Very High): 97 fps, Handbrake video transcoding: 3 minutes 39 seconds
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` (sentence-transformers) — produces 384-dimensional embeddings, runs entirely locally without API keys or rate limits, and loads in under 2 seconds. Well-suited for English-language semantic similarity tasks.

**Production tradeoff reflection:**
- **Cost:** Free and local vs. API-based models (OpenAI text-embedding-3-small, Cohere embed-v3) that charge per token. For a small corpus, local is clearly better; at scale, API models may offer better quality per dollar.
- **Context length:** 256 tokens max input — sufficient for 800-char chunks but would truncate longer passages. Models like nomic-embed-text support 8192 tokens for larger chunks.
- **Multilingual:** English-focused; for multilingual corpora, `paraphrase-multilingual-MiniLM-L12-v2` would be needed.
- **Quality vs. speed:** Larger models like `all-mpnet-base-v2` (768 dims) offer better accuracy at the cost of 2x embedding time and storage. For 209 chunks the difference is negligible, but at millions of chunks it matters.
- **Local vs. API-hosted:** Local models have zero latency for embedding but require GPU/CPU resources. API-hosted models offload compute but add network latency and a dependency on external services.

### Retrieval Test Results

**Query 1:** "What are the main cons of the Microsoft Surface Pro 11th Edition?"

| Rank | Source | Distance | Content Preview |
|------|--------|----------|-----------------|
| 1 | surface_pro_11.txt | 0.535 | Title and specs section |
| 2 | surface_pro_11.txt | 0.575 | Cons list and verdict |
| 3 | surface_pro_11.txt | 0.662 | Software and compatibility |
| 4 | surface_pro_11.txt | 0.777 | Battery life section |
| 5 | surface_pro_11.txt | 0.852 | Keyboard friction issues |

All 5 results from the correct source. The top chunk (dist=0.535) contains the exact cons list. This works well because the query semantically matches the "cons" section directly — the word "cons" in the query aligns with the negative assessments in the chunk text. The document is self-contained enough that all chunks carry relevant context about the Surface Pro's drawbacks.

**Query 2:** "What GPU does the Dell XPS 14 use?"

| Rank | Source | Distance | Content Preview |
|------|--------|----------|-----------------|
| 1 | dell_xps_14_2024.txt | 0.693 | Title and specs (includes RTX 4050) |
| 2 | dell_xps_14_2024.txt | 0.802 | Thermals and pros/cons |
| 3 | gigabyte_g6x.txt | 0.826 | GPU wattage comparison |
| 4 | dell_xps_14_2024.txt | 0.861 | Design section |
| 5 | dell_g15_5520.txt | 0.868 | Dell G15 specs |

The top chunk correctly identifies the RTX 4050 GPU. The Gigabyte G6X chunk at rank 3 appeared because it discusses GPU wattage comparisons across laptops, which is semantically related to "GPU" but from a different laptop. This is expected cross-contamination that the LLM handles by checking the `[Source: ...]` labels injected into the context.

**Query 3:** "How does the HP Victus 15 compare to the Acer Nitro 5?"

| Rank | Source | Distance | Content Preview |
|------|--------|----------|-----------------|
| 1 | hp_victus_15.txt | 0.439 | Pros/cons and comparison |
| 2 | hp_victus_15.txt | 0.480 | Verdict with Nitro 5 comparison |
| 3 | hp_victus_15.txt | 0.632 | Title and overview |
| 4 | dell_g15_5520.txt | 0.677 | Budget gaming context |
| 5 | hp_victus_15.txt | 0.770 | Display limitations |

Excellent retrieval — the top 2 results (dist < 0.5) contain the direct Victus-vs-Nitro 5 comparison text from the review's verdict section. The reviewer explicitly compared the two laptops, so the embedding model correctly identified high semantic similarity between the query and these comparison passages.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a helpful laptop review assistant. Answer the user's question using ONLY the
information provided in the context below. Do not use your general training knowledge.

If the provided context does not contain enough information to answer, respond with:
'I don't have enough information on that based on the available documents.'

Always cite which document(s) your answer draws from by mentioning the source filename.
```

**How source attribution is surfaced in the response:**

Grounding is enforced through two mechanisms:
1. **System prompt restriction:** The instruction explicitly forbids using training knowledge and specifies a fallback response for insufficient context, preventing hallucination. Requiring citations forces the model to tie each claim to a specific document.
2. **Source labels in context:** Each chunk is prefixed with `[Source: filename]` when injected into the LLM prompt, so the model knows which document each fact comes from and can attribute accordingly.

**Verification:** When asked "What is the price of the iPhone 16 Pro?" (not in any document), the system correctly responds: "I don't have enough information on that based on the available documents."

### Example Responses

**Example 1 — In-scope query:**

> **Q:** What are the main cons of the Microsoft Surface Pro 11th Edition?
>
> **A:** The main cons of the Microsoft Surface Pro 11th Edition, as stated in the surface_pro_11.txt document, are:
> 1. Shallow keyboard with poor tactile feedback
> 2. Poor trackpad with inconsistent click feel
> 3. Limited port selection with no USB-A or headphone jack
> 4. Expensive when factoring in keyboard accessory cost
> 5. Essentially a glorified tablet running Windows 11
>
> **Sources:** surface_pro_11.txt

**Example 2 — Comparative query:**

> **Q:** How does the HP Victus 15 compare to the Acer Nitro 5 for budget gaming?
>
> **A:** Based on the information provided in the hp_victus_15.txt files, the HP Victus 15 is outperformed by the Acer Nitro 5 in terms of gaming performance, particularly due to the Acer Nitro 5's superior RTX 30-series graphics. The reviewer notes that the Acer Nitro 5 frequently offers better value at similar or slightly higher prices. The Acer Nitro 5 has a Geekbench 5.4 score of 9,148 compared to the HP Victus 15's score of 6,902. Overall, the Acer Nitro 5 seems to be a better option for budget gaming, but the HP Victus 15 may still be suitable for casual gamers on a tight budget at a discounted price below $700.
>
> **Sources:** hp_victus_15.txt, dell_g15_5520.txt

**Example 3 — Out-of-scope query (refusal):**

> **Q:** What is the price of the iPhone 16 Pro?
>
> **A:** I don't have enough information on that based on the available documents.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the battery life of the MacBook Air 15 M3? | 15 hours 3 minutes at 150 nits | "The battery life is around 13 hours and 4 minutes when web surfing at 150 nits. This is a 4-minute increase over the M2 model." (Source: macbook_air_15_m3.txt) | Partially relevant | Partially accurate |
| 2 | What GPU does the Dell XPS 14 2024 use and how does it perform in games? | RTX 4050, 6GB VRAM; Shadow of the Tomb Raider 50 fps, Civ VI 88 fps | "Uses an Nvidia GeForce RTX 4050 (6GB VRAM). Achieved 68 fps at 1080p and 85 fps in Borderlands 3." (Sources: dell_xps_14_2024.txt, gigabyte_g6x.txt) | Partially relevant | Partially accurate |
| 3 | What are the main cons of the Microsoft Surface Pro 11th Edition? | Shallow keyboard, poor trackpad, limited ports, expensive | "1. Shallow keyboard with poor tactile feedback 2. Poor trackpad with inconsistent click feel 3. Limited port selection with no USB-A or headphone jack 4. Expensive when factoring in keyboard accessory cost 5. Essentially a glorified tablet." (Source: surface_pro_11.txt) | Relevant | Accurate |
| 4 | How does the HP Victus 15 compare to the Acer Nitro 5 for budget gaming? | Victus thinner but weaker GPU; Nitro 5 better value | "The HP Victus 15 is outperformed by the Acer Nitro 5 due to superior RTX 30-series graphics. Nitro 5 Geekbench: 9,148 vs Victus: 6,902. Nitro 5 offers better value. Victus suits casual gamers below $700." (Source: hp_victus_15.txt) | Relevant | Accurate |
| 5 | What is the display brightness of the Lenovo Yoga Slim 7x in SDR mode? | 464 nits SDR, 785 nits HDR peak | "The display brightness in SDR mode is 464 nits." (Source: lenovo_yoga_slim_7x.txt) | Relevant | Accurate |

**Overall: 3/5 accurate, 2/5 partially accurate, 0/5 inaccurate.**

---

## Failure Case Analysis

**Question that failed:** What is the battery life of the MacBook Air 15 M3?

**What the system returned:** "The battery life of the MacBook Air 15 M3 is around 13 hours and 4 minutes when web surfing at 150 nits." The correct answer is 15 hours and 3 minutes.

**Root cause (tied to a specific pipeline stage):** The failure occurred at the **chunking stage**. The MacBook Air review states "The battery lasted 15 hours and 3 minutes on continuous web surfing at 150 nits" as a single sentence, but the 800-character chunking split this sentence across two chunks. The retrieved chunk started with "web surfing at 150 nits. This is a modest 4-minute increase over the M2 model" — it contained the tail end of the battery section but not the leading "15 hours and 3 minutes" figure. The LLM then incorrectly inferred the battery life was 13 hours 4 minutes, which was actually the MSI Prestige competitor's battery life mentioned later in the same chunk as a comparison.

**What you would change to fix it:** Increase the overlap from 150 to 200+ characters to ensure that key facts near chunk boundaries are captured in both adjacent chunks. Alternatively, switch to sentence-aware chunking that avoids splitting mid-sentence, ensuring complete facts stay within a single chunk.

---

**Second failure — Q2 cross-document contamination:**

**Question that failed:** What GPU does the Dell XPS 14 2024 use and how does it perform in games?

**What the system returned:** Correctly identified the RTX 4050 6GB VRAM, but cited benchmark numbers from the Gigabyte G6X review (68 fps, 85 fps in Borderlands 3) instead of the Dell XPS 14's actual numbers (50 fps in Shadow of the Tomb Raider, 88 fps in Civ VI).

**Root cause (tied to a specific pipeline stage):** The failure occurred at the **retrieval stage**. The top-ranked chunk (distance 0.648) was from `gigabyte_g6x.txt`, which discussed GPU wattage comparisons and included benchmark numbers. This chunk ranked higher than the Dell XPS 14's own gaming benchmark chunk because the Gigabyte review used more GPU-specific terminology. The LLM then blended facts from both sources despite the `[Source: ...]` labels being present.

**What you would change to fix it:** Add a stronger system prompt instruction like "never combine facts from different source documents in a single claim" or implement source-aware re-ranking that boosts chunks from the document mentioned in the query.

---

## Spec Reflection

**One way the spec helped you during implementation:**
The chunking strategy section in planning.md forced me to reason about chunk sizes before writing code. By analyzing that the reviews were medium-to-long form (600–3,700 words) with distinct sections, I chose 800-character chunks with 150-character overlap. This upfront analysis prevented the trial-and-error of starting with arbitrary values and debugging poor retrieval later. When I ran ingest.py and got 209 chunks in the target range (50–2,000), I knew the strategy was sound without needing to iterate.

**One way your implementation diverged from the spec, and why:**
The original plan specified scraping reviews from RTINGS.com and The Verge, but both sites rendered content via JavaScript, making simple HTTP requests return only navigation menus instead of review text. I pivoted to Laptop Mag as an alternative source for 6 of the 12 reviews. This was not planned in the spec, but it actually produced better results — Laptop Mag reviews are consistently structured with clear sections (specs, display, performance, battery, verdict), which made chunking more effective than the less predictable content structure from the originally planned sources.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I provided Claude Code with my 12 review URLs and asked it to write a Python scraping script using `requests` and `BeautifulSoup` with site-specific extractors for Tom's Hardware, RTINGS, and The Verge.
- *What it produced:* Claude generated a complete `scrape_reviews.py` with three extraction functions, one per site. The Tom's Hardware extractor worked well (2,400–3,700 words per review), but the RTINGS and Verge extractors returned only navigation menus (~197 words) because those sites render content via JavaScript.
- *What I changed or overrode:* I directed Claude to abandon the RTINGS/Verge URLs and instead search for equivalent reviews on Laptop Mag, which serves content in static HTML. I reviewed each alternative URL Claude found to ensure it was a full review (not a deals post or comparison article) before approving the scrape. This pivot from the original spec was my decision based on the scraping results.

**Instance 2**

- *What I gave the AI:* After running ingest.py, I asked Claude to print 5 random chunks and check them for quality issues like HTML artifacts, navigation text, or fragments.
- *What it produced:* Claude ran the script and identified that chunks from Tom's Hardware reviews contained "(Image credit: Tom's Hardware)" text and "Latest Videos From" boilerplate that survived the initial cleaning pass.
- *What I changed or overrode:* I directed Claude to add specific regex cleaning rules: `re.sub(r'\(Image credit:[^)]*\)', '', text)` and `re.sub(r'Latest Videos From.*', '', text)`. I verified the fix by re-running ingest.py and manually inspecting the sample chunks to confirm the artifacts were gone before proceeding to embedding. I also added cleaning rules for "Swipe to scroll horizontally" and "Row N - Cell N" table artifacts that I noticed in the output.

---

## Query Interface

The system uses a Gradio web UI accessible at `http://localhost:7860`.

**Input:** A single text box labeled "Your question" with a placeholder example ("e.g. What is the battery life of the MacBook Air 15 M3?") and an orange "Ask" button. Users can also press Enter to submit.

**Output:** Two text areas — "Answer" displays the grounded response with source citations, and "Sources used" lists all document filenames that contributed to the answer.

**Sample interaction transcript:**
1. User types: "What is the display brightness of the Lenovo Yoga Slim 7x in SDR mode?"
2. User clicks "Ask"
3. Answer box shows: "The display brightness of the Lenovo Yoga Slim 7x in SDR mode is 464 nits. (Source: lenovo_yoga_slim_7x.txt)"
4. Sources box shows: "- lenovo_yoga_slim_7x.txt"
