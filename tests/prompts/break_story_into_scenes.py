from prompts import BreakStoryIntoScenesPrompt
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()

class TestBreakStoryIntoScenes(TestCase):
        

    
        def test_empty(self):
            out = BreakStoryIntoScenesPrompt(
                story="""Once upon a time, in a lush jungle kingdom, there lived a mighty ruler named King Moocha Raja. His palace was grand, and his heart, kind. One sunny afternoon, a clever little monkey spied an open window to the king's chamber and thought it the perfect chance for an adventure.

Sneaking inside, the monkey discovered King Moocha Raja fast asleep, snoring louder than a thunderstorm! Quietly, the monkey picked up a large palm leaf and began to fan the sleeping king. The cool breeze was so pleasant that the king slept more peacefully than ever before.

When he awoke, King Moocha Raja was surprised to see his new furry friend. He chuckled with delight and named the monkey Munchkin. The king and Munchkin quickly became the best of pals. Every day the monkey entertained the king with acrobatic tricks and was rewarded with juicy fruits and tiny royal clothes.

But not everyone was pleased. The king’s ministers scowled at the monkey, not liking the special attention he received.

One ill-fated morning, as Munchkin and the king were playing in the royal chambers, a mischievous fly buzzed around the king's nose. Trying to help, Munchkin aimed to swat the fly away but accidentally thumped the king’s nose instead!

"Ouch!" howled the king, his nose red with surprise and anger. "Away with you!" he commanded, feeling betrayed.

Munchkin's heart sank, and with a sad little squeak, he scampered away.

Time passed, and King Moocha Raja's nose healed, but his heart ached for his dear friend. He realized his rash decision was too harsh. The king ordered a search for Munchkin, but the monkey was nowhere to be found.

Finally, the king went to the open window and called out, “Munchkin, my friend, if you are near, know that I am sorry!”

To his joy, Munchkin emerged from a nearby tree. The king welcomed him back with a warm hug, promising always to be a fair and kind friend.

And so, King Moocha Raja and Munchkin were reunited, sharing many more days of laughter and friendship in the grand kingdom, where every window stayed open, just in case.
""",
                characters="""[{
"name": "Moocha Raja",
"description": "(full body:1.2), Indian king in rich, elaborate royal attire and jewelry, (standing:1.2) in his opulent, ornately decorated palace bedroom, thoughtful expression, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
}, {
"name": "The Monkey",
"description": "(full body:1.2), Playful monkey in a miniature coat and pants, (standing:1.2) in the royal court next to Moocha Raja, mischievous yet affectionate expression, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
}, {
"name": "The Maid",
"description": "(full body:1.2), Young maid in traditional Indian servant attire, (standing:1.2) in Moocha Raja's bedroom, fanning the king, look of dedication, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
}]""",
                

                debug=True
            )
            print(out)


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