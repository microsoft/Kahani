from unittest import TestCase
from prompts import GenerateScenesPrompt
from api import SDAPI
import base64
from PIL import Image
import io
import PIL
import base64
from dotenv import load_dotenv
load_dotenv()

class TestGenerateSceneImage(TestCase):
    def test_empty(self):
        prompt = "Bala (boy in a bright-colored shirt and shorts, running joyfully, wide smile, eyes focused on dog), Simba (golden-furred dog, bounding after waves, tail high, looks playful), Marina Beach alive with kite-flyers, Chennai skyline, vendors, families, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        
        
        with open("canny_bb_scene0.png", "rb") as f:
            conditioned_image = f.read()
            conditioned_image = base64.b64encode(conditioned_image).decode("utf-8")
       
        with open("tests/prompts/Generate_scene/bala_pose_one.png", "rb") as f:
            first_ref_img = f.read()
            first_ref_img = base64.b64encode(first_ref_img).decode("utf-8")
       
        with open("tests/prompts/Generate_scene/simba_pose_one.png", "rb") as f:
            second_ref_img = f.read()
            second_ref_img = base64.b64encode(second_ref_img).decode("utf-8")
       
        image_data = SDAPI.reference_image(conditioned_image=conditioned_image,first_ref_image=first_ref_img,second_ref_image=second_ref_img, prompt=prompt, seed=0, steps=40)
 
        img_data = base64.b64decode(image_data)
        with open(f"final_scene_testing.png", "wb") as f:
            f.write(img_data)
            
           
            