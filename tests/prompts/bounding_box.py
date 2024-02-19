from prompts import BoundingBoxPrompt
from unittest import TestCase
from dotenv import load_dotenv

load_dotenv()


class TestBoundimgBox(TestCase):
    def test_empty(self):
        out = BoundingBoxPrompt(
            backdrop="The lush greenery of a jungle with the grandeur of the king's palace in the background. An open window is visible.",
            characters="""
                King Moocha Raja: Lying comfortably, snoring with royal abandon.,
                Munchkin: Tiptoeing with wide, curious eyes, reaching for a palm leaf.""",
            narration="There once was a king named Moocha Raja, who had a gigantic, fancy palace. A monkey named Munchkin sneaked in for some fun!",
            debug=True,
        )
        print(out)
