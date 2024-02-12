from functools import partial
import base64
import io
import PIL
import gradio as gr
from gradio.data_classes import FileData
import os
import time

import openai
from llm import llm, sm, um
from kahani import Kahani
from dotenv import load_dotenv
from api import SDAPI
from uuid import uuid4
load_dotenv()

local_dir = partial(os.path.join, os.path.dirname(__file__), "outputs")


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def bot(history):
    user_input = history[-1][0]
    history[-1][1] = ""

    k = Kahani()
    k.input = user_input

    for chunk in k.extract_culture():
        history[-1][1] += chunk
        yield history

    history.append([None, None])
    history[-1][1] = "... Generating Image ..."
    yield history

    prompt = "small girl in the forest, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
    out = SDAPI.text2image(prompt=prompt)
    out = base64.b64decode(out)
    out = PIL.Image.open(io.BytesIO(out))
    path = local_dir(f"{uuid4()}.png")
    out.save(path, 'PNG')
    history[-1][1] = (path, prompt)
    yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(
            None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
        likeable=False
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter",
            container=False,
        )

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True),
                 None, [txt], queue=False)

demo.queue()
if __name__ == "__main__":
    demo.launch()
