from unittest import TestCase
from prompts import ExtractCharactersPrompt
from dotenv import load_dotenv
load_dotenv()

class TestExtractCharacters(TestCase):
    
        def test_empty(self):
            out = ExtractCharactersPrompt(
                story="""Once upon a time, in the warm and sunny land of Kerala, there lived a little girl named Sruthi. She had a smile like the morning sun and a laugh that reminded everyone of the gentle waves at the nearby Kovalam beach. Sruthi loved many things, but if you asked her to pick her favorite, she would giggle and say, "Halwa, of course!" She adored the sweet, sticky treat that her Amma made, flavored with cardamom and ghee. One bright day, Sruthi saw a moving van parked next to her house. "Amma, we have new neighbors!" she exclaimed with excitement. "Yes, dear. That's Kumar uncle's family. They're moving in today," her Amma replied with a warm smile. Sruthi wanted to welcome them. She knew how good it felt to make friends and the importance of being kind to neighbors. So, with a little help from her Amma, Sruthi made the softest, most delicious halwa and decorated it with cashew nuts that looked like little stars. With a plate full of halwa, Sruthi shyly knocked on Kumar uncle's door. "Namaste, I'm Sruthi. Welcome to our neighborhood!" she said, offering the halwa. Kumar uncle's eyes twinkled like the evening stars over Kovalam. "Thank you, little one. Your kindness is as sweet as this delightful halwa," he said, taking a small bite. "And from today, you have a new friend right next door. From that day forward, Sruthi and Kumar uncle became good friends. He would tell her stories of the ocean, and she would share more halwa, made with love and kindness. And the neighbors all around learned the gentle power of kindness and the joy of welcoming friends with open hearts and sweet treats.""",
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