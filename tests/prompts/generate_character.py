from unittest import TestCase
from prompts import GenerateCharactersPrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCharacters(TestCase):
    
        def test_empty(self):
            out = GenerateCharactersPrompt(
                description = "A mighty ruler with a kind heart, likely regal in appearance with a grand attire befitting of a jungle king. His features may include a gentle face marked with the wisdom of leadership.",
                debug=True
            )
    
            print(out)