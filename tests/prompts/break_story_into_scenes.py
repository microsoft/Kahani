from prompts import BreakStoryIntoScenesPrompt
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()

class TestBreakStoryIntoScenes(TestCase):
        

    
        def test_empty(self):
            out = BreakStoryIntoScenesPrompt(
                story="""Once upon a time, in the warm and sunny land of Kerala, there lived a little girl named Sruthi. She had a smile like the morning sun and a laugh that reminded everyone of the gentle waves at the nearby Kovalam beach.
Sruthi loved many things, but if you asked her to pick her favorite, she would giggle and say, "Halwa, of course!" She adored the sweet, sticky treat that her Amma made, flavored with cardamom and ghee.
One bright day, Sruthi saw a moving van parked next to her house. "Amma, we have new neighbors!" she exclaimed with excitement.
"Yes, dear. That's Kumar uncle's family. They're moving in today," her Amma replied with a warm smile.
Sruthi wanted to welcome them. She knew how good it felt to make friends and the importance of being kind to neighbors. So, with a little help from her Amma, Sruthi made the softest, most delicious halwa and decorated it with cashew nuts that looked like little stars.
With a plate full of halwa, Sruthi shyly knocked on Kumar uncle's door. "Namaste, I'm Sruthi. Welcome to our neighborhood!" she said, offering the halwa.
Kumar uncle's eyes twinkled like the evening stars over Kovalam. "Thank you, little one. Your kindness is as sweet as this delightful halwa," he said, taking a small bite. "And from today, you have a new friend right next door."
""",
                characters="""[{"name":"Sruthi","description":"A joyful girl from Kovalam beach, Kerala, about 9 years old with dark brown skin and shoulder-length curly black hair, usually tied in a ponytail with a green ribbon. She often wears a bright yellow sundress with little blue wave patterns, reflecting the beach beside her village."}, 
{"name":"Sruthi's Amma","description":"A woman from Kovalam beach, Kerala, in her mid-30s with long straight black hair typically pulled back into a neat bun. She has a warm brown skin tone and frequently wears a light green cotton sari with a violet border and a matching blouse, her attire echoing the lushness of her garden."}, 
{"name":"Kumar Kaka","description":"A cheerful man from Kovalam beach, Kerala, in his early 50s with light brown skin and a head of thick, slightly graying hair. He sports a friendly mustache and prefers wearing a cream-colored shirt paired with a sky-blue lungi, embodying the casual warmth of seaside living."}]
""",
                debug=True,
                stream=True
            )
            # print(out)
            for chunk in out:
                print(chunk, end="")


# output for above input
# [
#   {
#     "narration": "In the heart of a vibrant jungle, King Moocha Raja snoozed under the hot sun, when a curious monkey sneaked in for some fun!",
#     "backdrop": "A luxurious chamber with an open window, sunlight streaming in, lush jungle visible outside.",
#     "characters": {
#       "King Moocha Raja": "Lying on a lavish bed, asleep, a peaceful expression on his face.",
#       "The Monkey": "Tiptoeing inside, eyes wide with curiosity, holding a large palm leaf, starting to fan the king."
#     }
#   },
#   {
#     "narration": "The king laughed with joy at his new pal, decking out Munchkin in tiny royal apparel!",
#     "backdrop": "The grandeur of the palace's main hall, with servants and ministers milling about.",
#     "characters": {
#       "King Moocha Raja": "Sitting on his throne, chuckling, watching the monkey do tricks, clapping his hands in delight.",
#       "The Monkey": "Dressed in his new royal clothes, performing acrobatics, enjoying the spotlight with a happy grin."
#     }
#   },
#   {
#     "narration": "A single clap turned cheers to screams, as Munchkin's swat hit more than just a fly, it seems!",
#     "backdrop": "Inside the royal chambers, opulent decor around, with a tension-filled atmosphere.",
#     "characters": {
#       "King Moocha Raja": "Startled, holding his red nose with pain and shock on his face, standing up in annoyance.",
#       "The Monkey": "Mid-swat with a look of panic realizing the mistake, horror replacing the previous mischief."
#     }
#   },
#   {
#     "narration": "With an open heart and an open window, the king's call for forgiveness made their friendship regrow!",
#     "backdrop": "The same chamber, window wide open, soft light of dusk filling the room, a serene jungle in the background.",
#     "characters": {
#       "King Moocha Raja": "Leaning out the window, eyes hopeful, hands cupped around his mouth, calling out.",
#       "The Monkey": "Emerging from a tree, cautious yet hopeful, moving towards the king's open arms."
#     }
#   }
# ]