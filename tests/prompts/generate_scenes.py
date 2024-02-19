from unittest import TestCase
from prompts import GenerateScenesPrompt
from api import SDAPI
import base64
from PIL import Image
import io
import PIL
import base64
from dotenv import load_dotenv
load_dotenv()

class TestGenerateStory(TestCase):
    def test_empty(self):
        out = GenerateScenesPrompt(
            backdrop="The lush greenery of a jungle with the grandeur of the king's palace in the background. An open window is visible.",
            cultural_context="""- The presence of a king indicates a hierarchical societal structure, possibly a monarchy that values royal lineage and authority.
- The name "Moocha Raja" suggests a South Asian culture, with "Raja" being a title for a monarch, historically used in the Indian subcontinent.
- A monkey as a significant character points towards regions where monkeys are indigenous and culturally significant, such as India where monkeys are often associated with the Hindu deity Hanuman.
- The exchange of fruits and clothes between the king and the monkey indicates a traditional system of patronage and reward for service rendered.
- The unfavorable view of the monkey by the king's ministers reflects a class or caste distinction, possibly hinting at tension between established court protocol and non-traditional elements.
- Animal fables are a common element in South Asian folklore, which often carry moral lessons about power, friendship, and forgiveness.
- The final reconciliation could reflect cultural values of mercy, recognizing faults, and the value of companionship over protocol.""",
            character_actions="",
            scene="""{
    "narration": "There once was a king named Moocha Raja, who had a gigantic, fancy palace. A monkey named Munchkin sneaked in for some fun!",
    "backdrop": "The lush greenery of a jungle with the grandeur of the king's palace in the background. An open window is visible.",
    "characters": {
      "King Moocha Raja": "Lying comfortably, snoring with royal abandon.",
      "Munchkin": "Tiptoeing with wide, curious eyes, reaching for a palm leaf."
    }
  }""",
            characters=""" {
      "King Moocha Raja": "Lying comfortably, snoring with royal abandon.",
      "Munchkin": "Tiptoeing with wide, curious eyes, reaching for a palm leaf."
    }""",
            narration="There once was a king named Moocha Raja, who had a gigantic, fancy palace. A monkey named Munchkin sneaked in for some fun!",
            debug=True
            
        )
        print("here is the output")
        print(out)

        # image = SDAPI.text2image(prompt=out, seed=42, steps=50)
        # print("here is the image")
        # print(image)

        # if image:
        #     print("Opening image")
        #     with open("out.png", "wb") as f:
        #         f.write(image)
        #     output = base64.b64decode(image)
        #     output = PIL.Image.open(io.BytesIO(image))
        #     output.show()
            
           
            