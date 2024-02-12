import gradio as gr
import os
import time

import openai
from llm import llm, sm, um
from kahani import Kahani
from dotenv import load_dotenv
load_dotenv()


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def bot(history):
    user_input = history[-1][0]
    history[-1][1] = ""
    # for chunk in llm([
    #     sm("You are a helpful assistant."),
    #     um(user_input)
    # ], stream=True):
    #     history[-1][1] += chunk
    #     yield history

    k = Kahani()
    k.input = user_input

    for chunk in k.extract_culture():
        history[-1][1] += chunk
        yield history

    # history.append([None,"My next message"])
    # yield history

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
