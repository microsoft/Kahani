import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()


class TestCannyImage(TestCase):

    def test_canny_scene_0(self):
        file_name = "tests/prompts/Generate_scene/Generate_canny_image/scene0_bounding_box.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_scene/Generate_canny_image/canny_bb_scene0.png", "wb") as f:
                f.write(img_data)
                
    def test_canny(self):
        file_name = "tests/prompts/Generate_scene/Generate_canny_image/scene_0_bounding_box_test.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_scene/Generate_canny_image/canny_bb_test.png", "wb") as f:
                f.write(img_data)
