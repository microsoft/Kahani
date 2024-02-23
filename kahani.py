import ast
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
from utils import final_scene_generation_prompt, modify_scene_pose_generation_prompt
from functools import partial
from PIL import Image
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
            yield "text", False, chunk
        self.db.cultural_context = full_cultural_context
        print(colored(f"\n\nCultural Context: {self.db.cultural_context}", color='blue'))
    
    def summarize_culture(self):
        print(colored('\nsummarizing cultural context\n', color='blue'))

        cultural_context = SummariseCulturePrompt(
            cultural_context=self.db.cultural_context,
            stream=True, callback=self.print_llm_output)
        culture_summary = ""
        for chunk in cultural_context:
            culture_summary += chunk
            yield "text", False, chunk
        self.db.cultural_context = culture_summary
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
            yield "text", False, chunk
        self.db.story = full_story
        print(colored(f"\n\nStory: {self.db.story}", color='blue'))
        
    def generate_character_image(self):
        print(colored('\n\ngenerating character image', color='blue'))
        for index, character in enumerate(self.db.characters):
            prompt =  GenerateCharactersPrompt(description=character.description, stream=True, callback=self.print_llm_output)
            character_prompt = ""
            for chunk in prompt:
                character_prompt += chunk
                yield "text", False, chunk
            self.db.characters[index].prompt = character_prompt
            image = SDAPI.text2image(prompt=character_prompt, seed=0, steps=40)
            image = SDAPI.remove_background(image=image)
            if image:
                self.db.characters[index].image = image
                with open(self.local_dir(f"character_gen_{index}.png"), "wb") as f:
                    f.write(base64.b64decode(image))
                yield "file", True, self.local_dir(f"character_gen_{index}.png"), character_prompt
            print(colored(f"character: {self.db.characters[index]}", color='blue'))

    def extract_characters_from_story(self):
        print(colored('\n\nextracting characters', color='blue'))

        characters_generator = ExtractCharactersPrompt(story=self.db.story,
                                             stream=True, callback=self.print_llm_output)
        character_string=""
        for chunk in characters_generator:
            character_string += chunk
            yield "text", False, chunk
        try:
            characters = json.loads(character_string)
            self.db.characters = [Character(**c) for c in characters]
        except Exception as e:
            print(colored(f"error extracting characters: {e}", color='red'))
        print(colored(f"characters extracted from story: {self.db.characters}", color='blue'))
    
    def break_story_into_scenes(self):
        print(colored('\n\nbreaking story into scenes', color='blue'))
        scene_generator = BreakStoryIntoScenesPrompt(story=self.db.story, characters=[c.name for c in self.db.characters], stream=True, callback=self.print_llm_output)
        
        full_story_scene = ""
        for chunk in scene_generator:
            full_story_scene += chunk
            yield "text", False, chunk
        
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
        
    def generate_character_pose(self, index, image, narration):
        print(colored('\n\ngenerating character pose for particular scene', color='blue'))        
        image_data = SDAPI.pose_generation(image, prompt=f"{narration}, (Kids illustration, Pixar style:1.2), masterpiece, sharp focus, highly detailed, cartoon", seed=0, steps=40)
        if image_data:
            return image_data
    
    def generate_canny_image(self, image):
        print(colored('\n\ngenerating canny image', color='blue'))
        image_data = SDAPI.controlnet(init_images=[image])
        if image_data:
            return image_data

    def generate_bb_image(self):
        print(colored('\n\ngenerating bounding box for particular scene', color='blue'))
        for s, scene in enumerate(self.db.scenes):
            print(colored('\n\ngenerating bounding box', color='blue'))
            images = []
            dimensions = []
            bb_string = self.db.scenes[s].bounding_box
            narration = self.db.scenes[s].narration
                # Load the images of the characters based on the file naming convention
            for box in bb_string:
                character = box["character"]
                file_path = self.local_dir(f"scene{s}_{character}.png")  # Construct the file path
                try:
                    image = Image.open(file_path)
                    if image.mode != 'RGBA':
                        image = image.convert('RGBA')
                    images.append(image)
                        # images.append(Image.open(file_path))
                except FileNotFoundError:
                    print(f"File {file_path} not found.")
                    continue  # Skip this iteration if the file is not found

                dimensions_str = box["dimensions"]
                if isinstance(dimensions_str, str):
                    dimensions_list = ast.literal_eval(dimensions_str)
                else:
                    dimensions_list = dimensions_str

                dimensions.append([
                    int(dimensions_list[0]),
                    int(dimensions_list[1]),
                    int(dimensions_list[2]),
                    int(dimensions_list[3])
                ])

            # Create a new image with a black background
            canvas = Image.new('RGBA', (1280, 960), (0, 0, 0, 255))

                # Resize the images to fit the bounding boxes
            for i in range(len(images)):
                images[i] = images[i].resize((dimensions[i][2], dimensions[i][3]))

            # Paste the resized images onto the canvas at the specified coordinates
            for i in range(len(images)):
                canvas.paste(images[i], (dimensions[i][0], dimensions[i][1]), images[i])  
            final_image_path = self.local_dir(f"scene_{s}_bounding_box.png")
            canvas.save(final_image_path, "PNG")
            yield "file", True, final_image_path, narration
               
    def generate_bounding_box(self):
        for s, scene in enumerate(self.db.scenes):
            print(colored('\n\ngenerating bounding box', color='blue'))
            backdrop = self.db.scenes[s].backdrop
            narration = self.db.scenes[s].narration
            characters = self.db.scenes[s].characters
            print("inside bounding box generation function")
            bounding_box = BoundingBoxPrompt(backdrop = backdrop,narration=narration,characters=characters, stream=True, callback=self.print_llm_output)
            bb_string = ""
            for chunk in bounding_box:
                bb_string += chunk
                yield "text", False, chunk
            try:
                bb_string = json.loads(bb_string)
                self.db.scenes[s].bounding_box = bb_string
                print(colored(f"bounding_box: {bb_string}", color='blue'))
            except Exception as e:
                print(colored(f"error extracting bounding box: {e}", color='red'))
                    
    def generate_scene(self):
        for s, scene in enumerate(self.db.scenes):
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
                        prompt = modify_scene_pose_generation_prompt(original_prompt=original_prompt,pose=pose,facial_expression=facial_expression)
                        self.db.characters[i].scene_prompt[s] = prompt
                        image_data =self.generate_character_pose(c, c.image, narration=prompt)
                        image_data = SDAPI.remove_background(image=image_data)
                        self.db.characters[i].image_pose[s] = image_data
                        with open(self.local_dir(f"scene{s}_{name}.png"), "wb") as f:
                            f.write(base64.b64decode(image_data))
                        yield "file", True, self.local_dir(f"scene{s}_{name}.png"), prompt
    
    def final_scene_generation(self):
        for s, scene in enumerate(self.db.scenes):
            character_reference_images = []
            for character in scene.characters:
                for c in self.db.characters:
                    if c.name == character:
                        file_path = self.local_dir(f"scene{s}_character_{c.name}.png")
                        with open (file_path, "wb") as f:
                            f.write(base64.b64decode(c.image_pose[s]))
                        character_reference_images.append(file_path)
            names = []
            prompts = []
            for name, action in self.db.scenes[s].characters.items():
                for i, c in enumerate(self.db.characters):
                    if c.name == name:
                        names.append(name)
                        prompts.append(c.scene_prompt[s])
            print("this is the scene prompt taken for final scene genration", prompts)
            prompt = final_scene_generation_prompt(names, prompts) 
            backdrop = self.db.scenes[s].backdrop
            narration = self.db.scenes[s].narration
            final_prompt = GenerateScenesPrompt(characters=prompt, narration=narration, backdrop=backdrop, stream=True, callback=self.print_llm_output) 
            full_final_prompt = ""
            for chunk in final_prompt:
                full_final_prompt += chunk
            print("final_prompt", full_final_prompt)
            image_path = self.local_dir(f"scene_{s}_bounding_box.png")
            with open(image_path, "rb") as f:
                conditioned_image = f.read()
                conditioned_image = base64.b64encode(conditioned_image).decode("utf-8")
            print("calling controlnet here for canny bb")
            reference_canny_img = SDAPI.controlnet(init_images=[conditioned_image])
            
            if(len(character_reference_images) > 0):
                first_ref_img = character_reference_images[0]
            if(len(character_reference_images) > 1):  
                second_ref_img = character_reference_images[1]
            if(len(character_reference_images) == 1):
                second_ref_img = first_ref_img
            print("calling API here")
            print("final prompt input", full_final_prompt)
            image_data = SDAPI.reference_image(conditioned_image=reference_canny_img,first_ref_image=first_ref_img,second_ref_image=second_ref_img, prompt=full_final_prompt, seed=0, steps=40)
            self.db.scenes[s].image = image_data
            with open(self.local_dir(f"final_scene{s}.png"), "wb") as f:
                f.write(base64.b64decode(image_data))
            yield "file", True, self.local_dir(f"final_scene{s}.png"), full_final_prompt
        
    def save_db(self):
        with open(self.local_dir('db.json'), 'w') as f:
            f.write(self.db.model_dump_json(exclude_none=True))

    def sync_scenes_in_db(self, image, index):
        self.db.scenes[index].image = image
        self.save_db()
        print(f"-------- scene {index} synced ----------")

    
    
    