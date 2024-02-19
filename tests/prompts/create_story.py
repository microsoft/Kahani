from unittest import TestCase
from prompts import CreateStoryPrompt
from dotenv import load_dotenv
load_dotenv()

class TestCreateStory(TestCase):
    
        def test_empty(self):
            out = CreateStoryPrompt(
                story="",
                cultural_context="",
                user_input="""Write a story where a monkey sneaks into King Moocha Raja's bedroom through an open window. The monkey starts fanning the king while he sleeps, and they become friends. The king likes the monkey and gives it fruits and clothes. But the king's ministers don't like the monkey. One day, the monkey tries to hit a fly on the king's nose and hurts the king by mistake. The king gets mad and sends the monkey away. Later, the king feels bad and misses the monkey, so he tries to get it back. In the end, they reunite and the king realizes he was too harsh.""",
                debug=True
            )
    
            print(out)
    
       