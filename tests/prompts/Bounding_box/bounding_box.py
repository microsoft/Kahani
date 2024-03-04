from prompts import BoundingBoxPrompt
from unittest import TestCase
from dotenv import load_dotenv

load_dotenv()


class TestBoundingBox(TestCase):
    def test_first_scene(self):
        out = BoundingBoxPrompt(
            narration= "Bala, with his shiny dark hair, and Simba, the golden-furred dog, sprint along Marina Beach. The sand tickles their feet and paws.",
            backdrop="The wide expanse of Marina Beach is alive with bright skies and kite-flyers. The Chennai skyline looms in the distance, while vendors and families dot the shore.",
            characters=""" {
"Bala": "running joyfully, wide smile, eyes focused on Simba",
"Simba": "bounding after waves, tail high and wagging, looks playful"
}
""",
            images="""{
"Bala": "tests/prompts/Bounding_box/scene0_Bala.png",
"Simba": "tests/prompts/Bounding_box/scene0_Simba.png"
}""",
            stream=True,
            debug=True,
        )
        bounding_box_dimensions = ""
        for chunk in out:
            bounding_box_dimensions += chunk
        print(bounding_box_dimensions)   
        
    def test_second_scene(self):
        out = BoundingBoxPrompt(
            narration= "As the sky glows with sunset colors, Bala and Simba share a peaceful moment, surrounded by the soothing sounds of the beach.",
            backdrop="A serene sunset with orange and pink hues, traditional boats in the water, families around wearing colorful clothes, a palm tree providing shade.",
            characters="""  {
"Bala": "sitting under the palm tree, handing a piece of murukku to Simba, content smile",
"Simba": "sitting beside Bala, tilting head to take the snack, looking happy and at ease"
}""",
            images="""{
"Bala": "tests/prompts/Bounding_box/scene1_Bala.png",
"Simba": "tests/prompts/Bounding_box/scene1_Simba.png"
}""",
            stream=True,
            debug=True,
        )
        bounding_box_dimensions = ""
        for chunk in out:
            bounding_box_dimensions += chunk
        print(bounding_box_dimensions) 