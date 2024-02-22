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

class TestGenerateStory(TestCase):
    def test_empty(self):
        out = GenerateScenesPrompt(
            backdrop="A lush forest path leading to a heavy laden jamun tree with sunlight filtering through the leaves. Nearby stream visible with clear water",
            narration="In the heart of BR Hills, Geetha is on her quest for jamuns, basket in hand. The forest is alive with songs of the Soliga. Suddenly, she spots Mr. Monkey amidst the trees!",
            characters="""[
    {"name": "Geetha", "description": "A young, bright-eyed girl from BR Hills, known for her colorful skirts and joyous demeanor. Her love for jamuns is as vivid as her playful nature,(marching with basket) in a forest with jamun trees, (a look of determination)"},
    {"name": "Mr.Monkey", "description": "A mischievous monkey residing in the jamun trees of BR Hills, with the habit of tossing jamuns to his friends, (hanging from a tree branch) in a forest,( holding a jamun with a cheeky grin)"}]""",
            stream =True,
            debug=True
            
        )
        full_prompt = ""
        for chunk in out:
            full_prompt += chunk
            
        print(full_prompt)

        # image = SDAPI.text2image(prompt=out, seed=42, steps=50)
        # print("here is the image")
        # print(image)

        # if image:
        #     print("Opening image")
        #     with open("out.png", "wb") as f:
        #         f.write(image)
        #     output = base64.b64decode(image)
        #     output = PIL.Image.open(io.BytesIO(image))
        #     output.show()
            
           
            