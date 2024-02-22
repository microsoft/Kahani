import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()


class TestTexttoImage(TestCase):

    def testTexttoImage(self):
        user_input = "(full body:1.5), New neighbor male from Kerala, early 50s, dark complexion in a crisp, white shirt tucked into a cream-colored traditional wrap-around skirt with a golden border (veshti), short salt-and-pepper hair, (standing:1.5) in the lush green Kerala backyard with coconut trees, (Neutral face expression), looking at the camera, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        out = SDAPI.text2image(prompt = user_input)
        img_data = base64.b64decode(out)
        with open(f"output.png", "wb") as f:
                f.write(img_data)
