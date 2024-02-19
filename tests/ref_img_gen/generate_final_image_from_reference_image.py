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
        with open('prompt.txt', 'r') as file:
            prompt = file.read().strip()
        
        with open("reference_scene_image.png", "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
        
        out = SDAPI.reference_image(prompt=prompt,init_images=[img_data] )
        img_data = base64.b64decode(out)
        with open(f"output.png", "wb") as f:
            f.write(img_data) 
          
           
            

    