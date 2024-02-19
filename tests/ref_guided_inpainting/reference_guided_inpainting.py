import base64
from api import SDAPI
import unittest
from functools import partial
import os

folder_location = partial(os.path.join, os.path.dirname(__file__))

class TestReferenceGuidedInpainting(unittest.TestCase):
    
    def test_reference_guided_inpainting(self):
        with open(folder_location('prompt.txt'), 'r') as file:
            prompt = file.read().strip()

        with open(folder_location("monkey.png"), "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")

        with open(folder_location("pagri.jpg"), "rb") as f:
            ref_data = f.read()
            ref_data = base64.b64encode(ref_data).decode("utf-8")

        with open(folder_location("mask_turban.png"), "rb") as f:
            mask_data = f.read()
            mask_data = base64.b64encode(mask_data).decode("utf-8")

        image = SDAPI.reference_guided_inpainting(
            prompt=prompt,
            steps=35,
            width=1024,
            height=768,
            mask_blur=4,
            denoising_strength=0.9,
            init_images=[img_data],
            ref=ref_data,
            mask=mask_data
        )

        with open(folder_location("output.png"), "wb") as f:
            f.write(base64.b64decode(image))


if __name__ == '__main__':
    unittest.main()
