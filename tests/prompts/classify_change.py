from unittest import TestCase
from prompts import ClassifyChangePrompt

class TestClassifyChange(TestCase):
        def test_empty(self):
            out = ClassifyChangePrompt(
                story="""Salma's summer days are full of sunshine and joy as she visits her beloved Abu in the bustling city. She excitedly packs her bag, her heart fluttering like the wings of a hummingbird with anticipation. 

Her culture teaches her to hold elders in high esteem, and the thought of being with Abu fills her with warmth, much like the sun-drenched streets they will soon explore together. With her background, possibly from a warm corner of the Middle East or the vibrant lands of South Asia, the city's heat feels like a cozy embrace.

Hand-in-hand with Abu, they wander through colorful markets, the air rich with the scent of spices and the melody of laughter. Here, time with family is a precious gem, more valuable than the shiniest bauble in the bazaar. 

Together, they see towering buildings reaching for the sky, watch people from all walks of life, and share stories as sweet as the mangoes they enjoy from a street vendor. Salma listens, rapt, to tales from Abu's youth, each story a tapestry woven with the threads of wisdom and love.

For Salma, this holiday isn't just about visiting new places; it's a time to reinforce the beautiful bond she shares with her Abu. A bond as dear and enduring as the traditions that dance through her family's history. And in this season of unity and learning, the city's warmth is rivaled only by the love that shines in Abu's eyes.""",
                characters="""Salma": "Sitting cross-legged, joyfully examining the contents of the chest, with a background of the setting sun casting a warm glow on her findings.""",
                scenes="""""",
            )
            print(out)
