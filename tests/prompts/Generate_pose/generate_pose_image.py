import base64
from api import SDAPI
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()

class TestGeneratePoseImage(TestCase):
    
    def test_character_pose(self):
        prompt = "(full body:1.5), young boy from Chennai, 9, sun-kissed brown skin in a bright yellow T-shirt, navy blue shorts with white stripes, short, curly dark brown hair, (running:1.5) on Marina Beach, (bright smile, looking back:1.5),looking at the camera,(Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/bala_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"bala_pose_one.png", "wb") as f:
                f.write(img_data)
                
    #test on other scenarios
        
    def test_pose_one(self):
        prompt = "(full body:1.5), Golden Retriever at the Beach, young, golden coat in sun-kissed shimmer, rich chocolate brown eyes, (galloping joyfully towards the sea:1.5) on the sandy shore, (tongue hanging out, ears perked up, eyes wide with excitement:1.5), looking at the camera, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/simba_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"simba_pose_one.png", "wb") as f:
                f.write(img_data)
                
    def test_pose_two(self):
        prompt = "(full body:1.5), young boy from Chennai, age 9, sun-kissed brown skin in a bright yellow T-shirt and navy blue shorts with white stripes, short, curly dark brown hair, (casual walking posture, slightly slumped but content:1.5) on the Marina Beach, (smiling warmly with a hint of tiredness:1.5), looking at the camera, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/bala_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"bala_pose_two.png", "wb") as f:
                f.write(img_data)
                
    def test_pose_three(self):
        prompt = "(full body:1.5), Fluffy Golden Dog at the Suburban Park, Adult, Golden coat shimmering in the sunlight, with perky ears, and rich chocolate brown eyes, (Walking closely beside a person, tail slightly wagging:1.5) in the grassy fields of the suburban park, (Content and slightly tired expression with occasional yawns:1.5), looking at the camera, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/simba_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"simba_pose_two.png", "wb") as f:
                f.write(img_data)
                
    # Add more tests for testing API parameters for other scenarios
    def test_pose_bala(self):
        prompt = "(full body:1.5), boy from Chennai, 10 years, light brown skin in red and white striped cotton T-shirt paired with navy blue shorts, short curly black hair, (running joyfully:1.5) on the Marina Beach, (wide smile:1.5), looking at Simba, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/bala_api_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"api_bala.png", "wb") as f:
                f.write(img_data)     
    
    # Add more tests for testing image generation after restricting prompt tokens
    def test_bala(self):
        prompt = "(full body:1.5), boy from Chennai, 9, sun-kissed brown skin in bright yellow T-shirt, navy blue shorts with white stripes, short, curly dark brown hair, (walking tiredly but happy:1.5) on Marina Beach, (holding a shell, lively brown eyes glistening with joy:1.5), (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/bala_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"bala_token.png", "wb") as f:
                f.write(img_data)
                
    def test_simba(self):
        prompt = "(full body:1.5), Fluffy Golden Dog at Countryside, golden coat, perky ears, chocolate brown eyes, (laying down posture:1.5) on the green grass under sunlight, (content and tired expression with a yawn:1.5), (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        file_name = "tests/prompts/Generate_pose/simba_ref_img.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"simba_token.png", "wb") as f:
                f.write(img_data)
                
    
    def test_duplicate_char(self):
        prompt = "(full body:1.5), boy from Chennai beach, 10, light brown, in bright yellow T-shirt, navy blue shorts, short messy black hair, seated on the sand, (sharing sundal:1.5) in the beach environment, (happy and content:1.5), (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon"
        
        file_name = "tests/prompts/Generate_pose/inputs/character_gen_Bala.png"
        with open(file_name, "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            out = SDAPI.pose_generation(reference_image=img_data, prompt=prompt, seed=0, steps=40)
            out = SDAPI.remove_background(image=out)

            # print(out)
            img_data = base64.b64decode(out)
            with open(f"tests/prompts/Generate_pose/outputs/scene_Bala_test.png", "wb") as f:
                f.write(img_data)  
        

       