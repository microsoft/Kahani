import base64
from PIL import Image
import numpy as np
from api import SDAPI
from io import BytesIO

def generate_bb_image(bounding_box,s, local_dir):
    print("generate_bb_image")
    images = []
    dimensions = []

    # Load the images of the characters based on the file naming convention
    for box in bounding_box:
        character = box["character"]
        file_path = local_dir(f"scene{s}_{character}.png")  # Construct the file path
        try:
            image = Image.open(file_path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            images.append(image)
            # images.append(Image.open(file_path))
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue  # Skip this iteration if the file is not found

        dimensions.append(box["dimensions"])  # x, y, width, height

    # Create a new image with a black background
    canvas = Image.new('RGBA', (1280, 960), (0, 0, 0, 255))

    # Resize the images to fit the bounding boxes
    for i in range(len(images)):
        images[i] = images[i].resize((dimensions[i][2], dimensions[i][3]))

    # Paste the resized images onto the canvas at the specified coordinates
    for i in range(len(images)):
        canvas.paste(images[i], (dimensions[i][0], dimensions[i][1]), images[i])

    # Returns the final composite image
    return canvas


def modify_scene_pose_generation_prompt(original_prompt, pose, facial_expression):
    modified_prompt_corrected = original_prompt.replace("(standing:1.2)", f"({pose})").replace("(Neutral face expression)", f"({facial_expression})")
    final_prompt = modified_prompt_corrected.replace(", looking at the camera", "")
    return final_prompt
    
def final_scene_generation_prompt(names, prompts):
    substring_to_remove = "(Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
    processed_prompts = [prompt.split(substring_to_remove)[0] for prompt in prompts]
    result = []
    for name, prompt in zip(names, processed_prompts):
        result.append({"name": name, "description": prompt})

    return result