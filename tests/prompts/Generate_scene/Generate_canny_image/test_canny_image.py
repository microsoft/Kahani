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

    def test_canny_bala(self):
        file_name = "tests/prompts/Generate_scene/Generate_canny_image/scene0_Bala.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_scene/Generate_canny_image/bala_bb.png", "wb") as f:
                f.write(img_data)
                
    def test_canny_simba(self):
        file_name = "tests/prompts/Generate_scene/Generate_canny_image/scene0_Simba.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_scene/Generate_canny_image/simba_bb.png", "wb") as f:
                f.write(img_data)
                
    # testing object detection sceneario
    def test_OD_bb(self):
        file_name = "tests/prompts/Generate_scene/Generate_canny_image/object_detection_bb.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_scene/inputs/object_detection_bb.png", "wb") as f:
                f.write(img_data)