from functools import partial
import base64
import io
import PIL
import gradio as gr
from gradio.data_classes import FileData
from prompts import *
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
local_dir = partial(os.path.join, os.path.dirname(
    __file__), "outputs", user_data)
os.makedirs(local_dir(), exist_ok=True)

def determine_intent(user_input):
    intent = UserInputPrompt(user_input=user_input,stream=True)
    user_intent = ""
    for chunk in intent:
        user_intent += chunk
        
    print("this is the user intent", user_intent)
    return user_intent


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def get_accordion_content(is_open):
    if is_open:
        with gr.Accordion("Advance Image Editing", open=False) as adv:
            gr.Markdown("## Draw a mask to make a fine-grain change to the image.")
            with gr.Row():
                gr.Markdown("### Select scene to fine-grain edits")
                d = gr.Dropdown([f"Scene {i+1}" for i in range(2)])

            imgeditor = gr.ImageEditor(
                interactive=True,
                crop_size="4:3",
                brush=gr.Brush(
                    default_size="15",
                    color_mode="fixed",
                    default_color="#000",
                )
            )

            with gr.Row():
                with gr.Column():
                    uadv = gr.Textbox(
                        lines=2, placeholder="Enter your message here...", scale=10)
                    badv = gr.Button("Fine-grain edits", variant="primary")
                with gr.Column():
                    op = gr.Image(label="Reference Image", type="pil")
    else:
        adv = None
    return adv
            
            
def bot(history):
    global show_accordion
    user_input = history[-1][0]
    user_intent = determine_intent(user_input)
    
    if user_intent == "edit":
        show_accordion = True
    
    adv = get_accordion_content(show_accordion)
    
    history[-1][1] = ""
    print("user_input", user_input)
    k = Kahani(local_dir())
    k.input = user_input
    steps = ["extract_culture", "summarize_culture", "write_story", "extract_characters_from_story", "generate_character_image", "break_story_into_scenes","generate_pose", "generate_bounding_box", "generate_bb_image", "final_scene_generation"]
    for step in steps:
        history[-1][1] = f"... {step.replace('_', ' ').title()} ...\n"
        for out in getattr(k, step)():
            if out[0] == "text":
                chunk = out[2]
                history[-1][1] += chunk
                yield history
            elif out[0] == "file":
                yield history
                path = out[2]
                alt_text = out[3]
                history.append([None, (path, alt_text)])
                yield history
                history.append([None, ""])
        history.append([None, None])


with gr.Blocks() as demo:
    gr.Markdown("# Kahani: Under the Hood")
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

    with gr.Row():
        gr.Examples(
            [
                "Write a story about Geetha who loves jamuns and lives in BR Hills",
                "Write a story about Roopa lives at the foothills of Dehradun and loves to eat mangoes",
                "Write a story about Bala and his pet dog Simba on Marina beach"
            ],
            txt
        )

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True),
                 None, [txt], queue=False)
    
    
    
    # accordion
    show_accordion = False
    adv = get_accordion_content(show_accordion)
    

demo.queue()
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080
    )
