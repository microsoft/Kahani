from unittest import TestCase
from prompts import CreateStoryPrompt
from dotenv import load_dotenv
load_dotenv()

class TestCreateStory(TestCase):
    
        def test_empty(self):
            out = CreateStoryPrompt(
                story="",
                user_input="Write a story about Sruthi and her new neighbor Kumar uncle. Sruthi who loves halwa and lives near Kovalam beach. Emphasize the importance of kindness to neighbors.",
                cultural_context=""" - Indian cultural setting, likely Southern India given the names and context.
- Sruthi, a common female name in India, suggests a local family-oriented character.
- "Kumar uncle" implies an elder male figure who is not a relative but is referred to with respect.
- Halwa, a sweet dish, indicates Indian culinary traditions.
- Living near Kovalam beach may suggest a coastal lifestyle possibly in Kerala. """,
                debug=True,
                stream=True
            )
    
            # print(out)
            for chunk in out:
                print(chunk, end="")
    
       