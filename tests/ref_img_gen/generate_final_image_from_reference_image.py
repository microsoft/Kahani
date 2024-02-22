from api import SDAPI
import base64
import json
from PIL import Image
import io
import PIL
import base64
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()
 
 
class TestReferenceGuidedInpainting(TestCase):
    #image generation from reference image
     def test_empty(self):  
        prompt = """Girl and Monkey,(young girl with bright eyes,colorful skirt, joyous demeanor,(marching with basket:1.2)),(mischievous monkey,(hanging from a tree branch, holding a jamun with a cheeky grin:1.2)),(lush forest path leading to a heavy laden jamun tree, sunlight filtering through the leaves, nearby stream with clear water),(Kids illustration, Pixar style:1.2)), masterpiece, sharp focus, highly detailed, cartoon"""
 
        with open("canny_bb.png", "rb") as f:
            conditioned_image = f.read()
            conditioned_image = base64.b64encode(conditioned_image).decode("utf-8")
       
        with open("scene0_Geetha_nobg.png", "rb") as f:
            first_ref_img = f.read()
            first_ref_img = base64.b64encode(first_ref_img).decode("utf-8")
       
        with open("scene1_Monkey_nobg.png", "rb") as f:
            second_ref_img = f.read()
            second_ref_img = base64.b64encode(second_ref_img).decode("utf-8")
       
        image_data = SDAPI.reference_image(conditioned_image=conditioned_image,first_ref_image=first_ref_img,second_ref_image=second_ref_img, prompt=prompt, seed=0, steps=40)
 
        img_data = base64.b64decode(image_data)
        with open(f"final_scene_testing.png", "wb") as f:
            f.write(img_data)