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
            
    def test_one(self):
        out = GenerateScenesPrompt(
            narration="In the morning light of Chennai, young Bala and his dog Simba start a day of adventure. They zip through lively streets, then reach Marina Beach, where kites fly and waves greet them.",
            backdrop="The first scene is at Marina Beach with a panorama of the ocean, the sun rising above the horizon, and the Chennai cityscape in the distance. Sand is littered with vibrant kites and the iconic Chennai palm trees are present. Stalls line the promenade, with distinct South Indian architectural motifs.",
            action="""{
"Bala": "running excitedly, a big smile on his face",
"Simba": "tongue out, tail wagging, running alongside Bala"
}
""",
            description="""[{"name":"Bala","description":"A jovial boy from Chennai, around 10 years old with a light brown complexion and short, curly black hair that bounces as he runs. He has lively, dark brown eyes filled with merriment. Bala wears a bright yellow cotton T-shirt paired with navy blue shorts that are practical for playful days at Marina Beach."},
{"name":"Simba","description":"A golden-furred dog with ears that perk up in curiosity and deep brown eyes that shine with loyalty. His coat is well-groomed, reflecting the golden sands of Chennai's Marina Beach."}]""",
            stream =True,
            debug=True
            
        )
        full_prompt = ""
        for chunk in out:
            full_prompt += chunk
            
        print(full_prompt)
           
            