from model import generate_image

import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

with gr.Blocks() as demo:
    gr.Markdown("# Your Fancy Image Generator")
    with gr.Row(equal_height=True):
        textbox = gr.Textbox(lines=1, show_label=False)
        button = gr.Button("Generate", variant="primary")
    image = gr.Image(height=250)
    
    button.click(
        generate_image,
        inputs=textbox,
        outputs=image,
    )

demo.launch(share=True)
