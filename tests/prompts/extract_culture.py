from unittest import TestCase
from prompts import ExtractCulturePrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCulture(TestCase):

    def test_empty(self):
        out = ExtractCulturePrompt(
            cultural_context=""" """,
            user_input="Write a story about Sruthi and her new neighbor Kumar uncle. Sruthi who loves halwa and lives near Kovalam beach. Emphasize the importance of kindness to neighbors.",
            debug=True,
            stream=True
        )
        for chunk in out:
            print(chunk, end="")
