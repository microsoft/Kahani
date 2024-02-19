from unittest import TestCase
from prompts import ExtractCharactersPrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCharacters(TestCase):
    
        def test_empty(self):
            out = ExtractCharactersPrompt(
                user_input="""Once upon a time, in a lush jungle kingdom, there lived a mighty ruler named King Moocha Raja. His palace was grand, and his heart, kind. One sunny afternoon, a clever little monkey spied an open window to the king's chamber and thought it the perfect chance for an adventure.

Sneaking inside, the monkey discovered King Moocha Raja fast asleep, snoring louder than a thunderstorm! Quietly, the monkey picked up a large palm leaf and began to fan the sleeping king. The cool breeze was so pleasant that the king slept more peacefully than ever before.

When he awoke, King Moocha Raja was surprised to see his new furry friend. He chuckled with delight and named the monkey Munchkin. The king and Munchkin quickly became the best of pals. Every day the monkey entertained the king with acrobatic tricks and was rewarded with juicy fruits and tiny royal clothes.

But not everyone was pleased. The king’s ministers scowled at the monkey, not liking the special attention he received.

One ill-fated morning, as Munchkin and the king were playing in the royal chambers, a mischievous fly buzzed around the king's nose. Trying to help, Munchkin aimed to swat the fly away but accidentally thumped the king’s nose instead!

"Ouch!" howled the king, his nose red with surprise and anger. "Away with you!" he commanded, feeling betrayed.

Munchkin's heart sank, and with a sad little squeak, he scampered away.

Time passed, and King Moocha Raja's nose healed, but his heart ached for his dear friend. He realized his rash decision was too harsh. The king ordered a search for Munchkin, but the monkey was nowhere to be found.

Finally, the king went to the open window and called out, “Munchkin, my friend, if you are near, know that I am sorry!”

To his joy, Munchkin emerged from a nearby tree. The king welcomed him back with a warm hug, promising always to be a fair and kind friend.

And so, King Moocha Raja and Munchkin were reunited, sharing many more days of laughter and friendship in the grand kingdom, where every window stayed open, just in case.""",
                debug=True
            )
    
            print(out)