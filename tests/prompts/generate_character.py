from unittest import TestCase
from prompts import GenerateCharactersPrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCharacters(TestCase):
    
        def test_empty(self):
            out = GenerateCharactersPrompt(
                description = "A new neighbor in his early 50s settled in Kerala, with a dark complexion and short salt-and-pepper hair. He is typically dressed in a crisp, white shirt that is neatly tucked into a traditional cream-colored veshti with a golden border",
                debug=True,
                stream=True
            )
            # print(out)
            for chunk in out:
                print(chunk, end="")
            print()

        # def test_empty(self):
        #     out = GenerateCharactersPrompt(
        #         description = "A cheerful girl from the coastal village near Kovalam Beach, known for her twinkling eyes, warm heart, and her special sweet, sticky halwa with cardamom and cashews.",
        #         story = "Once upon a wave-kissed time, in the snug coastal village near Kovalam Beach, there lived a cheerful girl named Sruthi. With twinkling eyes and a heart as warm as the sun that danced on the ocean waves, Sruthi was famous for two things: her love for the sweet, sticky halwa and her boundless kindness. Sruthi's halwa was not just a treat; it was a ribbon of joy woven through the community. Made with love, sprinkled with cardamom, and filled with cashews, it melted in your mouth as magically as a golden sunset melt into the sea. One sun-splashed day, as Sruthi strolled home with a batch of fresh halwa, she noticed her new neighbor—a shy, elderly man named Kumar uncle—watching the playful seagulls from his lonely porch. Sruthi's heart whispered like the gentle waves,'Atithi Devo Bhava' With a knock as soft as the sea breeze, Sruthi stood at Kumar uncle's door, offering a plate piled high with halwa. His eyes twinkled, much like hers, as an unexpected smile found its way to his lips. 'Oh, what delightful halwa! Thank you, my dear', he said, tasting not just the sweetness of the halwa but the sweetness of companionship. From then on, Kumar uncle wasn't just a neighbor; he was part of Sruthi's extended family. They would share stories of the sea, bask in the balmy breeze, and of course, relish halwa together. Sruthi's kind gesture rippled through the village, reminding everyone that a little sweetness goes a long way—not just the kind you eat, but the kind you live. And so, embraced by the coconut palms and sung to by the waves, Sruthi and her neighbors wove a tapestry of kindness that was as delightful and enduring as Kovalam's very own sandy shores.",
        #         debug=True,
        #         stream=True
        #     )

        #     for chunk in out:
        #         print(chunk, end="")
        #     print()