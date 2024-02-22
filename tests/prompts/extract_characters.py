from unittest import TestCase
from prompts import ExtractCharactersPrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCharacters(TestCase):
    
        def test_empty(self):
            out = ExtractCharactersPrompt(
                story="""Once upon a wave-kissed time, in the snug coastal village near Kovalam Beach, there lived a cheerful girl named Sruthi. With twinkling eyes and a heart as warm as the sun that danced on the ocean waves, Sruthi was famous for two things: her love for the sweet, sticky halwa and her boundless kindness. 

Sruthi's halwa was not just a treat; it was a ribbon of joy woven through the community. Made with love, sprinkled with cardamom, and filled with cashews, it melted in your mouth as magically as a golden sunset melt into the sea. 

One sun-splashed day, as Sruthi strolled home with a batch of fresh halwa, she noticed her new neighbor—a shy, elderly man named Kumar uncle—watching the playful seagulls from his lonely porch. Sruthi's heart whispered like the gentle waves, "Atithi Devo Bhava." 

With a knock as soft as the sea breeze, Sruthi stood at Kumar uncle's door, offering a plate piled high with halwa. His eyes twinkled, much like hers, as an unexpected smile found its way to his lips. "Oh, what delightful halwa! Thank you, my dear," he said, tasting not just the sweetness of the halwa but the sweetness of companionship. 

From then on, Kumar uncle wasn't just a neighbor; he was part of Sruthi's extended family. They would share stories of the sea, bask in the balmy breeze, and of course, relish halwa together. Sruthi's kind gesture rippled through the village, reminding everyone that a little sweetness goes a long way—not just the kind you eat, but the kind you live. 

And so, embraced by the coconut palms and sung to by the waves, Sruthi and her neighbors wove a tapestry of kindness that was as delightful and enduring as Kovalam's very own sandy shores. """,
                debug=True,
                stream=True
            )

            for chunk in out:
                print(chunk, end="")

        # def test_empty(self):
        #     out = ExtractCharactersPrompt(
        #         story="""In a village woven into the green embrace of the Skandagiri Hills lived a little girl named Geetha. She had a smile like the sun breaking through the clouds, and her heart was full of more kindness than the river was of water.One day, while wandering near the edge of the forest, Geetha came across a gentle elephant trapped in a thorny bush. It trumpeted softly, its large eyes filled with worry. Without a second thought, Geetha carefully helped free the elephant from the snare."Thank you," rumbled the elephant, who could speak the language of the heart. "I am Ananda, and I will not forget your kindness."That night, as Geetha sat outside her home, a soft light flickered near her. A firefly, glowing like a tiny star, danced in the air."I am Tara," the firefly buzzed, "I saw what you did for Ananda. You have a beautiful heart." From then on, Ananda and Tara became Geetha's faithful friends. They played hide and seek among the trees, and Tara lit up their path with her radiant light. Geetha shared stories of her village, taught Ananda village songs, and weaved flower garlands for Tara to wear.The villagers often spoke of the trio's friendship, a testament to the nobility of kindness. "When we offer help without expecting anything," Geetha said, "friendship blooms like the lotus in the muddy waters. Friendship is the greatest treasure." And under the vast dome of the Southern Indian sky, amid the chorus of crickets and the whisper of the trees, the bonds of an unexpected friendship grew, teaching everyone around that in the heart of their biodiverse home, kindness was a language that all creatures understood.""",
        #         debug=True,
        #         stream=True
        #     )

        #     for chunk in out:
        #         print(chunk, end="")