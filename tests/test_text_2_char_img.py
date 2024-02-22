import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()


class TestTexttoImage(TestCase):

    def testTexttoImage(self):
        user_input = "(full body:1.2), Kovalam Beach elderly man, early 70s, with weathered skin in a light-colored mundu and a long-sleeved, button-up shirt, thinning white hair, (standing:1.2) at Kovalam Beach, (Neutral face expression), looking at the camera, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        out = SDAPI.text2image(prompt = user_input)
        img_data = base64.b64decode(out)
        with open(f"output.png", "wb") as f:
                f.write(img_data)
