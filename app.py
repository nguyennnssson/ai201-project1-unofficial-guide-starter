import gradio as gr
from query import ask


def handle_query(question: str):
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(f"- {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="Laptop Review Guide") as demo:
    gr.Markdown("## Laptop Review Guide — Ask Anything About Laptops")
    gr.Markdown("Ask questions about laptop reviews from Tom's Hardware and Laptop Mag. "
                "Answers are grounded in real expert reviews.")

    inp = gr.Textbox(label="Your question", placeholder="e.g. What is the battery life of the MacBook Air 15 M3?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources used", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
