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
        prompt = "Girl and elephant, (young girl in a bright green lehenga (sitting cross-legged:1.2)), (Indian elephant (looking at Geetha with large, worried eyes)), (Thick Forest with a tangle of thorny bushes, suspenseful shadows filtering through the trees), (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        
        
        with open("tests/prompts/Generate_scene/canny_image.png", "rb") as f:
            conditioned_image = f.read()
            conditioned_image = base64.b64encode(conditioned_image).decode("utf-8")
       
        with open("tests/prompts/Generate_scene/Geetha_kneeling.png", "rb") as f:
            first_ref_img = f.read()
            first_ref_img = base64.b64encode(first_ref_img).decode("utf-8")
       
        with open("tests/prompts/Generate_scene/ananda_relieved.png", "rb") as f:
            second_ref_img = f.read()
            second_ref_img = base64.b64encode(second_ref_img).decode("utf-8")
       
        image_data = SDAPI.reference_image(conditioned_image=conditioned_image,first_ref_image=first_ref_img,second_ref_image=second_ref_img, prompt=prompt, seed=0, steps=40)
 
        img_data = base64.b64decode(image_data)
        with open(f"final_scene_testing.png", "wb") as f:
            f.write(img_data)
            
           
            