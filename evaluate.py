from query import ask

TEST_QUESTIONS = [
    {
        "question": "What is the battery life of the MacBook Air 15 M3?",
        "expected": "15 hours and 3 minutes on continuous web surfing at 150 nits",
    },
    {
        "question": "What GPU does the Dell XPS 14 2024 use and how does it perform in games?",
        "expected": "Nvidia GeForce RTX 4050 with 6GB VRAM; Shadow of the Tomb Raider at 50 fps, Civilization VI at 88 fps at 1080p",
    },
    {
        "question": "What are the main cons of the Microsoft Surface Pro 11th Edition?",
        "expected": "Shallow keyboard, poor trackpad, limited ports, expensive for tablet functionality",
    },
    {
        "question": "How does the HP Victus 15 compare to the Acer Nitro 5 for budget gaming?",
        "expected": "The Victus 15 is thinner/lighter but has a weaker GPU (GTX 1650 vs RTX 30-series), worse battery, and the Nitro 5 offers better value",
    },
    {
        "question": "What is the display brightness of the Lenovo Yoga Slim 7x in SDR mode?",
        "expected": "464 nits average in SDR, with peak HDR brightness of 785 nits",
    },
]

if __name__ == "__main__":
    for i, item in enumerate(TEST_QUESTIONS, 1):
        result = ask(item["question"])
        print(f"\nQ{i}: {item['question']}")
        print(f"Expected: {item['expected']}")
        print(f"Got: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print(f"Chunks retrieved:")
        for c in result["chunks"]:
            print(f"  [{c['source']}] dist={c['distance']:.3f}: {c['text'][:100]}...")
        print("---")
