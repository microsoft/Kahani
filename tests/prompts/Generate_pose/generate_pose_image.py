import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()

class TestGeneratePoseImage(TestCase):
    
    def test_character_pose(self):
        prompt = "(full body:1.5), young boy from Chennai, 9, sun-kissed brown skin in a bright yellow T-shirt, navy blue shorts with white stripes, short, curly dark brown hair, (running:1.5) on Marina Beach, (bright smile, looking back:1.5),looking at the camera,(Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/bala_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"bala_pose.png", "wb") as f:
                f.write(img_data)
                
        

       