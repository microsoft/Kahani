import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()



class TestRemoveBgImage(TestCase):

    def test_remove_bg_image(self):
        file_name = "scene0_Geetha.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.remove_background(image=img_data)
            # print(out)
            img_data = base64.b64decode(out)
            with open(f"canny_bb.png", "wb") as f:
                f.write(img_data)