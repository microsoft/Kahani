from unittest import TestCase
from prompts import GeneratePosePrompt
from dotenv import load_dotenv
load_dotenv()

class TestGeneratePose(TestCase):
    
        def test_empty(self):
            out = GeneratePosePrompt(
                description = "A young boy from Chennai, aged 9, with sun-kissed brown skin and a head of short, curly dark brown hair. Bala's eyes are a lively shade of brown, reflecting his energetic spirit. He usually wears a bright yellow T-shirt and navy blue shorts with white stripes on the sides, perfect for the warm beach weather and active days spent running around Marina Beach.",
                action = "running with a bright smile, looking back at Simba, shorts and a t-shirt with sandals, wind blowing his hair",
                debug=True,
                stream=True
            )
            prompt = ""
            for chunk in out:
                prompt += chunk
            print(prompt)
                
                
        # Testing on multiple other cases 
        
        def test_first(self):
            out = GeneratePosePrompt(
                description = "A fluffy dog with a golden coat that shimmers in the sunlight. Simba's ears are perky, and his round eyes a rich, chocolate brown which radiate joy and excitement.",
                action = "off leash, running towards the water, tongue out, ears perked up, very happy expression as he splashes water",
                debug=True,
                stream=True
            )
            prompt = ""
            for chunk in out:
                prompt += chunk
            print(prompt)
            
        def test_second(self):
            out = GeneratePosePrompt(
                description = "A young boy from Chennai, aged 9, with sun-kissed brown skin and a head of short, curly dark brown hair. Bala's eyes are a lively shade of brown, reflecting his energetic spirit. He usually wears a bright yellow T-shirt and navy blue shorts with white stripes on the sides, perfect for the warm beach weather and active days spent running around Marina Beach.",
                action = "walking tiredly but happy, holding a shell in one hand, the other hand resting on Simba’s back",
                debug=True,
                stream=True
            )
            prompt = ""
            for chunk in out:
                prompt += chunk
            print(prompt)
            
        def test_third(self):
            out = GeneratePosePrompt(
                description = "A fluffy dog with a golden coat that shimmers in the sunlight. Simba's ears are perky, and his round eyes a rich, chocolate brown which radiate joy and excitement.",
                action = "walking closely beside Bala, looks content and a bit tired, occasionally yawning",
                debug=True,
                stream=True
            )
            prompt = ""
            for chunk in out:
                prompt += chunk
            print(prompt)
        

       