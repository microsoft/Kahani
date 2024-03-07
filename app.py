from functools import partial
import base64
import io
import PIL
import gradio as gr
from gradio.data_classes import FileData
from prompts import *
import os
import time
from PIL import Image
from api import STANDARD_HEIGHT, STANDARD_WIDTH

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

isInpaintingComplete = False
def determine_intent(user_input):
    intent = UserInputPrompt(user_input=user_input, stream=True)
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
            gr.Markdown(
                "## Draw a mask to make a fine-grain change to the image.")
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


k = Kahani(local_dir())


def bot(history):
    global show_accordion
    user_input = history[-1][0]
    # user_intent = determine_intent(user_input)

    # if user_intent == "edit":
    #     show_accordion = True

    # adv = get_accordion_content(show_accordion)

    history[-1][1] = ""
    print("user_input", user_input)
    k.input = user_input
    steps = ["extract_culture", "summarize_culture", "write_story", "extract_characters_from_story", "generate_character_image",
             "break_story_into_scenes", "generate_pose", "generate_bounding_box", "generate_bb_image", "final_scene_generation","update_inpainted_image"]
    for step in steps:
        if step == "update_inpainted_image":
            while not isInpaintingComplete:
                time.sleep(1)
        print(f"Running {step}")
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


def construct_mask_bw(filepath):
    img = Image.open(filepath)
    img = img.convert("RGBA")
    img_data = list(img.getdata())
    new_img_data = [(0, 0, 0, 255) if pixel[3] == 0 else (
        255, 255, 255, 255) for pixel in img_data]
    img.putdata(new_img_data)
    img.save(filepath)


def inpainting(imgeditor, user_input, scene_number, ref_image):
    print("Starting inpainting")

    image = Image.fromarray(imgeditor['layers'][0])
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    with open(local_dir('mask_api.png'), 'wb') as f:
        f.write(image_bytes)

    construct_mask_bw(local_dir('mask_api.png'))
    scene_index = int(scene_number.split(" ")[1]) - 1

    with open(local_dir(f"final_scene{scene_index}.png"), "rb") as f:
        img_data = f.read()
        img_data = base64.b64encode(img_data).decode("utf-8")

    buffered = io.BytesIO()
    ref_image.save(buffered, format="PNG")
    ref_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    with Image.open(local_dir("mask_api.png")) as img:
        resized_img = img.resize((STANDARD_WIDTH, STANDARD_HEIGHT))
        resized_img.save(local_dir("mask_api.png"))

    with open(local_dir("mask_api.png"), "rb") as f:
        mask_data = f.read()
        mask_data = base64.b64encode(mask_data).decode("utf-8")

    user_input += " " + \
        "simple, masterpiece, highly detailed, photorealistic, pixar style, animated"

    images = SDAPI.reference_guided_inpainting(
        prompt=user_input,
        steps=35,
        width=STANDARD_WIDTH,
        height=STANDARD_HEIGHT,
        mask_blur=4,
        batch_size=1,
        denoising_strength=0.9,
        init_images=[img_data],
        ref=ref_data,
        mask=mask_data
    )

    out = images[0]
    base64_output = out
    img = Image.open(io.BytesIO(base64.b64decode(out)))

    # for i in range(len(images)):
    #     image = images[i]
    #     count += 1
    #     out = image
    #     base64_output.append(out)
    #     out_pil = PIL.Image.open(io.BytesIO(base64.b64decode(out)))
    #     output.append(out_pil)
    #     img_data = base64.b64decode(out)
    #     img = Image.open(io.BytesIO(img_data))
    #     img.save(kcache(f'output_{count}.png'), 'PNG')

    # print("Inpainting done, selecting best image")
    # best_img_index = int(llm_vision(base64_output))-1
    # best_img = base64_output[best_img_index]

    k.sync_scenes_in_db(base64_output, scene_index)
    

    with open(local_dir(f"final_scene{scene_index}.png"), "wb") as f:
        f.write(base64.b64decode(base64_output))

    images = []
    for scene in k.db.scenes:
        out = scene.image
        out = base64.b64decode(out)
        out = PIL.Image.open(io.BytesIO(out))
        images.append((out, scene.narration))

    print("Gallery reloaded")
    isInpaintingComplete = True
    # return images


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

        def select_image(image_index):
            print("Image changed")
            image_index = int(image_index.split(" ")[1]) - 1
            return {
                "background": local_dir(f"final_scene{image_index}.png"),
                "layers": [],
                "composite": None
            }

        d.change(fn=select_image, inputs=d, outputs=imgeditor)
        badv.click(fn=inpainting,
                   inputs=[imgeditor, uadv, d, op],
                #    outputs=g
                   )

    # accordion
    # show_accordion = False
    # adv = get_accordion_content(show_accordion)


demo.queue()
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=8080
    )
