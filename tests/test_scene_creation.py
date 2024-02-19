from PIL import Image
import base64
import json
import os
from unittest import TestCase
from prompts import BoundingBoxPrompt, GenerateCharactersPrompt
import cv2
from api import SDAPI
from functools import partial
from dotenv import load_dotenv
from utils import crop_image_to_largest_contour, crop_image_to_largest_contour2, concat_images
load_dotenv()

folder_location = partial(os.path.join, os.path.dirname(__file__), "images")


settings = {
    "steps": 40,
    "sampler_name":
    "DPM++ 2M Karras",
    "cfg_scale": 7,
    "width": 800,
    "height": 600,
    "refiner": "sd_xl_refiner_1.0",
    "refiner_-checkpoint": "7440042bbd",
    "refiner_switch_at": 0.8,
    "negative_prompt": "EasyNegative, blurry, (bad_prompt:0.8), (artist name, signature, watermark:1.4), (ugly:1.2), (worst quality, poor detail:1.4), (deformed iris, deformed pupils, semi-realistic, CGI, 3d, render, sketch, drawing, anime:1.4), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, lowres, error, worst quality, low quality, out of frame, username, NSFW"
}


class SceneCreationTest(TestCase):

    scene = "Boy looking at girl in the library."
    character1 = "A curly haired boy with a scar on his forehead"
    character2 = "A girl with bushy brown hair and buck teeth"

    character1scene1 = "looking happy"
    character2scene1 = "Weary eyes, looking down, sad"

    def test1(self):
        # create boy's image

        prompt = GenerateCharactersPrompt(
            description=self.character1)

        print(prompt)

        image = SDAPI.text2image(
            prompt=prompt,
            **settings
        )

        with open(folder_location("boy.png"), "wb") as f:
            f.write(base64.b64decode(image))
          
    def test2(self):
        # create girl's image

        prompt = GenerateCharactersPrompt(
            description=self.character2)

        print(prompt)

        image = SDAPI.text2image(
            prompt=prompt,
            **settings
        )

        with open(folder_location("girl.png"), "wb") as f:
            f.write(base64.b64decode(image))
    
    def testremove_bg(self):
        # remove background for boy and girl
        for name in ["Butterfly", "Geetha", "Firefly", "Fire2"]:

            source = f"{name}.png"
            destination = f"{name}_clean.png"

            with open(folder_location(source), "rb") as f:
                image = base64.b64encode(f.read()).decode("utf-8")

            image = SDAPI.remove_background(input_image=image)

            with open(folder_location(destination), "wb") as f:
                f.write(base64.b64decode(image))

    def testcanny(self):
        # canny images

        for name in ["Butterfly", "Geetha", "Firefly", "Fire2"]:

            source = f"{name}_clean.png"
            destination = f"{name}_canny.png"

            with open(folder_location(source), "rb") as f:
                image = base64.b64encode(f.read()).decode("utf-8")

            image = SDAPI.controlnet(init_images=[image])

            with open(folder_location(destination), "wb") as f:
                f.write(base64.b64decode(image))
  
    def test15(self):
        # modify the character pose -- chararacter1scene1 -- boy
        # DK - please do this
        # source = f"boy.png"
        # destination = f"boy_pose.png"
        
        for name in ["Geetha_initial"]:

            source = f"{name}_clean.png"
            destination = f"Geetha.png"

            with open(folder_location(source), "rb") as f:
                image = base64.b64encode(f.read()).decode("utf-8")
        
        # with open(folder_location("boy_clean.png"), "rb") as f:
        #     img_pose = base64.b64encode(f.read()).decode("utf-8")
            
            out = SDAPI.pose_generation(
                image, prompt=f"{self.character1scene1}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", **settings)
        
            with open(folder_location(destination), "wb") as f:
                f.write(base64.b64decode(out))
        

    def test16(self):
        # modify the character pose -- chararacter2scene1 -- girl
        # DK - please do this
        with open(folder_location("girl_clean.png"), "rb") as f:
            img_pose = base64.b64encode(f.read()).decode("utf-8")
            
        out = SDAPI.pose_generation(
            img_pose, prompt=f"{self.character2scene1}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", **settings)
        
        with open(folder_location("girl_pose.png"), "wb") as f:
            f.write(base64.b64decode(out))

    

    

 

    def test5(self):
        # crop images

        for name in ["Butterfly", "Geetha", "Firefly", "Fire2"]:

            source = f"{name}_canny.png"
            destination = f"{name}_cropped.png"

            image = cv2.imread(folder_location(source))

            image = crop_image_to_largest_contour2(image)

            cv2.imwrite(folder_location(destination), image)

    def test6(self):
        out = BoundingBoxPrompt(
            backdrop=self.scene,
            narration="Harry was enthusiastic to win the race,and Hermione felt sad to lose the race.",
            characters="""
Harry: {self.character1}
Hermione: {self.character2}
""",
            debug=True,
        )

        print(out)

        bboxes = json.loads(out)
        bboxes = [
            tuple(bbox['dimensions']) for bbox in bboxes
        ]
        print(bboxes)

    def test7(self):

        # bboxes = [(10, 0, 500, 960), (700, 0, 500, 960)]
        bboxes = [(100, 250, 300, 650), (700, 250, 300, 650)]

        image = concat_images(
            Image.open(folder_location("boy_cropped.png")),
            Image.open(folder_location("girl_cropped.png")),
            (1280, 960),
            *bboxes
        )

        image.save(folder_location("combined.png"))
        print("generated created image")

    def test8(self):

        with open(folder_location("combined.png"), "rb") as f:
            conditioned_image = base64.b64encode(f.read()).decode("utf-8")

        out = SDAPI.reference_image(
            conditioned_image, prompt=f"{self.scene}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", **settings)

        with open(folder_location("final.png"), "wb") as f:
            f.write(base64.b64decode(out))
