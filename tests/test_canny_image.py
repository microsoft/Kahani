import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()


class TestCannyImage(TestCase):

    def test_canny_image(self):
        file_name = "input.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.controlnet(init_images=[img_data])
            img_data = base64.b64decode(out)
            with open(f"output.png", "wb") as f:
                f.write(img_data)