from io import BytesIO
import os
from prompts import *
from pydantic import BaseModel
from transitions import Machine
import base64
from api import SDAPI
import json
from llm import fn, llm, sm, um
from models import Character, Scene, Story
from dotenv import load_dotenv
from enum import Enum
from termcolor import colored
from utils import final_scene_generation_prompt, generate_bb_image, modify_scene_pose_generation_prompt
from functools import partial
load_dotenv()


class ChangeType(Enum):
    CHARACTER = "character"
    SCENE = "scene"


class Change(BaseModel):

    type: ChangeType
    index: int | str
    change: str = None


class Kahani:

    db = None
    buffer: list[Change] = []
    input: str = None

    def __init__(self, outputs: str):
        self.db = Story()
        self.local_dir = partial(os.path.join, outputs)

        states = [
            "start",
            "update_culture",

            "create_story",
            "extract_characters",
            "generate_character_image",
            "extract_scenes",

            "classify_change",
            "update_dependencies",

            "process_changes",
            "done"
        ]

        transitions = [
            {"trigger": "advance", "source": "start",
                "dest": "update_culture", 'after': 'extract_culture'},

            {"trigger": "advance", "source": "update_culture",
                "dest": "create_story", "conditions": "is_story_empty", 'after': 'write_story'},
            {"trigger": "advance", "source": "create_story",
                "dest": "extract_characters", 'after': 'extract_characters_from_story'},
            {"trigger": "advance", "source": "extract_characters",
                "dest": "generate_character_image", 'after': 'generate_character_image'},
            {"trigger": "advance", "source": "generate_character_image",
                "dest": "extract_scenes", 'after': 'break_story_into_scenes'},
            # {"trigger": "advance", "source": "extract_scenes",
            #     "dest": "process_changes", "after": "process_changes"},
            
            # {"trigger": "advance", "source": "update_culture",
            #     "dest": "classify_change", 'after': 'classify_change'},
            # {"trigger": "advance", "source": "classify_change",
            #     "dest": "update_dependencies", "after": "update_dependencies"},
            # {"trigger": "advance", "source": "update_dependencies",
            #     "dest": "process_changes", "after": "process_changes"},

            # {"trigger": "advance", "source": "process_changes",
            #     "dest": "process_changes", "conditions": "are_changes_pending", "after": "process_changes"},
            {"trigger": "advance", "source": "extract_scenes",
                "dest": "done", "before": 'save_db'},

            {"trigger": "reset", "source": "*", "dest": "start"},

        ]

        Machine(model=self, states=states,
                transitions=transitions, initial=states[0])

    def print_llm_output(self, output):
        print(colored(output, color='yellow'), end='')

    def is_story_empty(self):
        return self.db.story is None

    def are_changes_pending(self):
        return len(self.buffer) > 0

    def extract_culture(self):
        print(colored('\n\nExtracting Culture', color='blue'))

        user_input = self.input

        cultural_context = ExtractCulturePrompt(
            cultural_context=self.db.cultural_context,
            user_input=user_input,
            stream=True, callback=self.print_llm_output)
        full_cultural_context = ""
        for chunk in cultural_context:
            full_cultural_context += chunk
            yield "text", chunk

        # print(colored('\nsummarizing cultural context\n', color='blue'))

        # cultural_context = SummariseCulturePrompt(
        #     cultural_context=cultural_context,
        #     stream=True, callback=self.print_llm_output)
        self.db.cultural_context = full_cultural_context
        print(colored(f"\n\nCultural Context: {self.db.cultural_context}", color='blue'))
        
    def classify_change(self):
        print(colored('\n\nclassifying change', color='blue'))

        self.buffer = []

        user_input = self.input
        action = ClassifyChangePrompt(
            story_status="Exists" if self.db.story is not None else "Does not exist",
            character_status=",".join([c.name for c in self.db.characters]) if len(
                self.db.characters) > 0 else "No",
            scene_status=len(self.db.scenes) > 0,
            user_input=user_input,
        )

        print(colored(action, color='blue'))

        if action['function'] == 'update_story':
            pass
        # self.write_story(user_input)
        elif action['function'] == 'update_character':
            self.buffer.append(Change(type=ChangeType.CHARACTER,
                                      index=action['arguments']['name'], change=action['arguments']['change']))
        elif action['function'] == 'update_scene':
            # self.update_scenes(user_input)
            self.buffer.append(Change(type=ChangeType.SCENE,
                                      index=action['arguments']['scene_number'], change=action['arguments']['change']))

    def update_dependencies(self):
        print(
            colored(f"\nupdating dependencies", color='blue'))

        for i in range(len(self.buffer)):
            if self.buffer[i].type == ChangeType.CHARACTER:
                name = self.buffer[i].index
                for c, scene in enumerate(self.db.scenes):
                    for name_key in scene.characters.keys():
                        if name == name_key:
                            self.buffer.append(Change(
                                type=ChangeType.SCENE, index=c, change=self.buffer[i].change)
                            )
            elif self.buffer[i].type == ChangeType.SCENE:
                # no op
                pass

        # TODO - dedupe the buffer

    def process_changes(self):
        print(
            colored(f"\nprocessing changes {len(self.buffer)}", color='blue'))

        if len(self.buffer) > 0:
            change = self.buffer.pop(0)

            # if change.type == ChangeType.CHARACTER:
            #     self.generate_character(change.index)
            # if change.type == ChangeType.SCENE:
            #     self.generating_scene(change.index, change=change.change)

    def write_story(self):
        print(colored('\n\nwriting story', color='blue'))

        user_input = self.input
        story = CreateStoryPrompt(
            story=self.db.story,
            cultural_context=self.db.cultural_context,
            user_input=user_input,
            stream=True, callback=self.print_llm_output)
        full_story = ""
        for chunk in story:
            full_story += chunk
            yield "text", chunk
        self.db.story = full_story
        print(colored(f"\n\nStory: {self.db.story}", color='blue'))
      
    # def single_character_prompt(self, character, index):
        
        # image = SDAPI.text2image(prompt=prompt, seed=0, steps=40)
        #     # TODO: remove background (model not available)
        #     # image = SDAPI.remove_background(input_image=image)
        # if image:
        #     self.db.characters[index].image = image
        #     with open(f"character_gen_{index}.png", "wb") as f:
        #         f.write(base64.b64decode(image))
        
    def generate_character_image(self):
        print(colored('\n\ngenerating character image', color='blue'))
        for index, character in enumerate(self.db.characters):
            prompt =  GenerateCharactersPrompt(description=character.description, stream=True, callback=self.print_llm_output)
            character_prompt = ""
            for chunk in prompt:
                character_prompt += chunk
                yield "text", chunk
            self.db.characters[index].prompt = character_prompt
            print(colored(f"character: {self.db.characters[index]}", color='blue'))
            image = SDAPI.text2image(prompt=character_prompt, seed=0, steps=40)
            # # TODO: remove background (model not available)
            # # image = SDAPI.remove_background(input_image=image)
            if image:
                self.db.characters[index].image = image
                with open(self.local_dir(f"character_gen_{index}.png"), "wb") as f:
                    f.write(base64.b64decode(image))
                yield "file", self.local_dir(f"character_gen_{index}.png"), character_prompt

    def extract_characters_from_story(self):
        print(colored('\n\nextracting characters', color='blue'))

        characters_generator = ExtractCharactersPrompt(story=self.db.story,
                                             stream=True, callback=self.print_llm_output)
        character_string=""
        for chunk in characters_generator:
            character_string += chunk
            yield "text", chunk
        
        try:
            characters = json.loads(character_string)
            self.db.characters = [Character(**c) for c in characters]
            print(colored(f"characters: {self.db.characters}", color='blue'))
        except Exception as e:
            print(colored(f"error extracting characters: {e}", color='red'))
    
    def break_story_into_scenes(self):
        print(colored('\n\nbreaking story into scenes', color='blue'))
        scene_generator = BreakStoryIntoScenesPrompt(story=self.db.story, characters=[c.name for c in self.db.characters], stream=True, callback=self.print_llm_output)
        
        full_story_scene = ""
        for chunk in scene_generator:
            full_story_scene += chunk
            yield "text", chunk
        
        print(colored(f"full_story_scene: {full_story_scene}", color='blue'))
        try:
            scenes = json.loads(full_story_scene)
            self.db.scenes = [Scene(**s) for s in scenes]
            print(colored(f"scenes: {self.db.scenes}", color='blue'))
        except Exception as e:
            print(colored(f"error extracting scenes: {e}", color='red'))
           
        for s, scene in enumerate(self.db.scenes):
            for character in scene.characters:
                for c in self.db.characters:
                    if c.name == character:
                        c.scenes.append(s)

            self.generate_scene(s)
        #     image = self.generate_bounding_box(s)
            
            # character_reference_images = []
            # for character in scene.characters:
            #     for c in self.db.characters:
            #         if c.name == character:
            #             file_path = f"scene{s}_pose_test_{c.name}.png"
            #             with open (file_path, "wb") as f:
            #                 f.write(base64.b64decode(c.image_pose))
            #             character_reference_images.append(file_path)
            
        #     buffered = BytesIO()
        #     # Save the image to the buffer in a standard format (PNG/JPEG)
        #     image.save(buffered, format="PNG")  # Using PNG to support transparency

        #     # Get the byte data from the buffer
        #     img_byte = buffered.getvalue()

                
        #     # # Encode the bytes to base64
        #     img_base64 = base64.b64encode(img_byte).decode("utf-8")
        #     prompts = []
        #     for name, action in self.db.scenes[s].characters.items():
        #         for i, c in enumerate(self.db.characters):
        #             if c.name == name:
        #                 prompts.append(c.scene_prompt)
        #     prompt = final_scene_generation_prompt(prompts,scene.backdrop)            
        #     self.final_scene_generation(s, prompt, img_base64, character_reference_images)
        
    def generate_character_pose(self, index, image, narration):
        print(colored('\n\ngenerating character pose for particular scene', color='blue'))        
        image_data = SDAPI.pose_generation(image, prompt=f"{narration}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", seed=0, steps=40)
        #TODO : remove background(model not available)
        # image_data = SDAPI.remove_background(input_image=image_data)
        if image_data:
            return image_data
    
    def generate_canny_image(self, image):
        print(colored('\n\ngenerating canny image', color='blue'))
        image_data = SDAPI.controlnet(init_images=[image])
        if image_data:
            return image_data
        
    def generate_bounding_box(self, s):
        print(colored('\n\ngenerating bounding box', color='blue'))
        backdrop = self.db.scenes[s].backdrop
        narration = self.db.scenes[s].narration
        characters = self.db.scenes[s].characters
        bounding_box = BoundingBoxPrompt(backdrop = backdrop,narration=narration,characters=characters, stream=True, callback=self.print_llm_output)
        bounding_box = json.loads(bounding_box)
        for character in self.db.scenes[s].characters:
            for c in self.db.characters:
                if c.name == character:
                    with open(f"scene_{s}_{c.name}_image_pose.png", "wb") as f:
                        f.write(base64.b64decode(c.image_pose))               
        image = generate_bb_image(bounding_box,s)
        return image
          
    def generate_scene(self, s, change=None):
        print(colored('\n\ngenerating scene', color='blue'))
        name = f"scene-{s}"
        character_actions = []
        for name, action in self.db.scenes[s].characters.items():
            for i, c in enumerate(self.db.characters):
                if c.name == name:
                    character_actions.append(
                        f"{name} ({c.description}): {action}")
                    parts = action.split(", ")
                    # Storing into two variables
                    if len(parts) >= 2:
                        pose = parts[0]
                        facial_expression = ", ".join(parts[1:])
                    else:
                        pose, facial_expression = action, "Neutral face expression"
                    original_prompt = c.prompt
                    print("name", name)
                    print("original_prompt", original_prompt)
                    print("pose", pose)
                    print("facial_expression", facial_expression)
                    prompt = modify_scene_pose_generation_prompt(original_prompt=original_prompt,pose=pose,facial_expression=facial_expression)
                    self.db.characters[i].scene_prompt = prompt
                    image_data =self.generate_character_pose(c, c.image, narration=prompt)
                    #TODO : remove background and canny (model not available)
                    # image_data = SDAPI.remove_background(image_data)
                    # image_data = self.generate_canny_image(image_data)  
                    self.db.characters[i].image_pose = image_data
    
    def final_scene_generation(self, s, prompt, conditioned_image, character_reference_images):
        if(len(character_reference_images) > 0):
            first_ref_img = character_reference_images[0]
        if(len(character_reference_images) > 1):  
            second_ref_img = character_reference_images[1]
        if(len(character_reference_images) == 1):
            second_ref_img = first_ref_img
        image_data = SDAPI.reference_image(conditioned_image=conditioned_image,first_ref_image=first_ref_img,second_ref_image=second_ref_img, prompt=f"{prompt}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", seed=0, steps=40)
        self.db.scenes[s].image = image_data
        
    def save_db(self):
        with open('db.json', 'w') as f:
            f.write(self.db.model_dump_json(exclude_none=True))

    def sync_scenes_in_db(self, image, index):
        self.db.scenes[index].image = image
        self.save_db()
        print(f"-------- scene {index} synced ----------")

    
    
    