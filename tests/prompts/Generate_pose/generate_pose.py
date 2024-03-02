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
                
        

       