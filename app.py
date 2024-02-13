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

user_data = str(uuid4())
local_dir = partial(os.path.join, os.path.dirname(__file__), "outputs", user_data)
os.makedirs(local_dir(), exist_ok=True)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def bot(history):
    user_input = history[-1][0]
    history[-1][1] = ""
    print("user_input", user_input)
    k = Kahani(local_dir())
    k.input = user_input
    
    steps = ["extract_culture", "write_story", "extract_characters_from_story","generate_character_image","break_story_into_scenes"]
    for step in steps:
        history[-1][1] = f"... {step.replace('_', ' ').title()} ...\n"
        for out in getattr(k, step)():
            if out[0] == "text":
                chunk = out[1]
                history[-1][1] += chunk
                yield history
            elif out[0] == "file":
                path = out[1]
                alt_text = out[2]
                history[-1][1] = (path, alt_text)
                yield history    
        history.append([None, None])

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(
            None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
        likeable=False,
        height=600
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
