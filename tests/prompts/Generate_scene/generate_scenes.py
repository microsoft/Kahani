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

class TestGenerateScene(TestCase):
    def test_empty(self):
        out = GenerateScenesPrompt(
            narration="Bala, with his shiny dark hair, and Simba, the golden-furred dog, sprint along Marina Beach. The sand tickles their feet and paws.",
            backdrop="The wide expanse of Marina Beach is alive with bright skies and kite-flyers. The Chennai skyline looms in the distance, while vendors and families dot the shore.",
            characters="""{
"Bala": "running joyfully, wide smile",
"Simba": "bounding after waves, tail high and wagging, looks playful"
}
""",
            stream =True,
            debug=True
            
        )
        full_prompt = ""
        for chunk in out:
            full_prompt += chunk
            
        print(full_prompt)
            
           
            