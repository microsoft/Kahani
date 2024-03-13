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
import numpy as np
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
            # yield "text", False, f"character: {character.name}"
            image = SDAPI.text2image(prompt=character_prompt, seed=0, steps=40)
            image = SDAPI.remove_background(image=image)
            if image:
                self.db.characters[index].image = image
                with open(self.local_dir(f"character_gen_{character.name}.png"), "wb") as f:
                    f.write(base64.b64decode(image))
                yield "file", True, self.local_dir(f"character_gen_{character.name}.png"), character_prompt
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
    
    def crop_image(self, input_path):
        print(colored('\n\ncropping image', color='blue'))
        img = Image.open(input_path)
        
        # Convert the image to a numpy array
        img_array = np.array(img)
        
        # Find the non-zero coordinates
        non_zero_coords = np.argwhere(img_array != 0)
        
        # Get the bounding box coordinates
        top_left = non_zero_coords.min(axis=0)
        bottom_right = non_zero_coords.max(axis=0)
        
        # Extract the part of the image within the bounding box
        cropped_image_array = img_array[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
        
        # Convert the numpy array back to an image
        cropped_img = Image.fromarray(cropped_image_array)
        
        # Save the cropped image, replacing the original image
        cropped_img.save(input_path)
     
    def resize_to_fit_bbox(self, img_shape, bbox_shape):
        # Calculate the scaling factors for each dimension
        scale_y = bbox_shape[0] / img_shape[0]
        scale_x = bbox_shape[1] / img_shape[1]

        # Use the smaller scaling factor to maintain the aspect ratio
        scale_factor = min(scale_y, scale_x)

        # Calculate the new dimensions
        new_height = int(img_shape[0] * scale_factor)
        new_width = int(img_shape[1] * scale_factor)

        return (new_height, new_width)   
    
    def generate_scene_canvas(self):
        print(colored('\n\ngenerating scene canvas', color='blue'))
        for s, scene in enumerate(self.db.scenes):
            print(colored('\n\ngenerating bounding box canvas', color='blue'))
            bounding_boxes = self.db.scenes[s].bounding_box
            narration = self.db.scenes[s].narration
            canvas = Image.new('RGB', (1280, 960), (0, 0, 0))

            for box in bounding_boxes:
                character = box["character"]
                dimensions = box["dimensions"]
                bbox_shape = dimensions[2:]
                file_path = self.local_dir(f"scene{s}_{character}.png")
                try:
                    img = Image.open(file_path)
                    img_shape = np.array(img).shape[:-1]
                    new_img_shape = self.resize_to_fit_bbox(img_shape, bbox_shape)
                    resized_img = img.resize((new_img_shape[1], new_img_shape[0]))
                    canvas.paste(resized_img, (dimensions[0], dimensions[1]))
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                    continue
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
                    
    def generate_pose(self):
        for s, scene in enumerate(self.db.scenes):
            print(colored('\n\ngenerating scene', color='blue'))
            name = f"scene-{s}"
            character_actions = []
            for name, action in self.db.scenes[s].characters.items():
                for i, c in enumerate(self.db.characters):
                    if c.name == name:
                        character_actions.append(
                            f"{name} ({c.description}): {action}")
                        prompt = GeneratePosePrompt(description=c.description, action=action, stream=True, callback=self.print_llm_output)
                        character_pose_prompt = ""
                        for chunk in prompt:
                            character_pose_prompt += chunk
                            yield "text", False, chunk
                        # yield "file", True, self.local_dir(f"character_gen_{c.name}.png"), "character_prompt"
                        with open (self.local_dir(f"character_gen_{c.name}.png"), "rb") as f:
                            ref_image = f.read()
                            ref_image = base64.b64encode(ref_image).decode("utf-8")
                        self.db.characters[i].scene_prompt[s] = character_pose_prompt
                        image_data =SDAPI.pose_generation(reference_image=ref_image, prompt=character_pose_prompt, seed=0, steps=40)
                        image_data = SDAPI.remove_background(image=image_data)
                        self.db.characters[i].image_pose[s] = image_data
                        with open(self.local_dir(f"scene{s}_{name}.png"), "wb") as f:
                            f.write(base64.b64decode(image_data))
                        self.crop_image(self.local_dir(f"scene{s}_{name}.png"))
                        yield "file", True, self.local_dir(f"scene{s}_{name}.png"), character_pose_prompt
    
    
    def final_scene_generation(self):
        print(colored('\n\nfinal scene generation', color='blue'))
        for s, scene in enumerate(self.db.scenes):
            character_reference_images = self.extract_character_images(scene, s)
            backdrop, narration, characters = self.extract_scene_details(scene)
            final_prompt = self.generate_final_prompt(characters, narration, backdrop)
            reference_canny_img = self.generate_reference_image(s)
            first_ref_img, second_ref_img = self.handle_reference_images(character_reference_images,s)
            print(colored('\n\ngenerating final scene image for final scenes', color='blue'))
            yield "text", False, final_prompt
            yield "file", True, self.local_dir(f"reference_image_scene{s}.png"), "reference image for scene"
            yield "file", True, first_ref_img, "first reference image for scene"
            yield "file", True, second_ref_img, "second reference image for scene"
            
            print("first_ref_img", first_ref_img)
            print("second_ref_img", second_ref_img)
            
            with open(self.local_dir(f"reference_image_scene{s}.png"), "rb") as f:
                final_ref = f.read()
                final_ref = base64.b64encode(final_ref).decode("utf-8")
                
            with open(first_ref_img, "rb") as f:
                final_first_img= f.read()
                final_first_img = base64.b64encode(final_first_img).decode("utf-8")
            
            with open(second_ref_img, "rb") as f:
                final_second_img= f.read()
                final_second_img = base64.b64encode(final_second_img).decode("utf-8")    
            
            image_data = SDAPI.reference_image(conditioned_image=final_ref, first_ref_image=final_first_img, second_ref_image=final_second_img, prompt=final_prompt)
            self.db.scenes[s].image = image_data
            with open(self.local_dir(f"final_scene{s}.png"), "wb") as f:
                f.write(base64.b64decode(image_data))
            yield "file", True, self.local_dir(f"final_scene{s}.png"), "final prompt because image does not work??"
            
    def extract_character_images(self, scene, scene_index):
        print(colored('\n\nextracting character images for final scenes', color='blue'))
        character_reference_images = []
        for character in scene.characters:
            for c in self.db.characters:
                if c.name == character:
                    file_path = self.local_dir(f"scene{scene_index}_character_{c.name}.png")
                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(c.image_pose[scene_index]))
                    character_reference_images.append(file_path)
        return character_reference_images

    def extract_scene_details(self, scene):
        print(colored('\n\nextracting scene details for final scenes', color='blue'))
        backdrop = scene.backdrop
        narration = scene.narration
        characters = scene.characters
        return backdrop, narration, characters

    def generate_final_prompt(self, characters, narration, backdrop):
        print(colored('\n\ngenerating final prompt for final scenes', color='blue'))
        final_prompt = GenerateScenesPrompt(characters=characters, narration=narration, backdrop=backdrop, stream=True, callback=self.print_llm_output)
        full_final_prompt = ""
        for chunk in final_prompt:
            full_final_prompt += chunk
        return full_final_prompt

    def generate_reference_image(self, scene_index):
        print(colored('\n\ngenerating reference image for final scenes', color='blue'))
        image_path = self.local_dir(f"scene_{scene_index}_bounding_box.png")
        with open(image_path, "rb") as f:
            conditioned_image = f.read()
            conditioned_image = base64.b64encode(conditioned_image).decode("utf-8")
        reference_canny_img = SDAPI.controlnet(init_images=[conditioned_image])
        reference_image = reference_canny_img
        with open(self.local_dir(f"reference_image_scene{scene_index}.png"), "wb") as f:
            f.write(base64.b64decode(reference_image))
        return reference_canny_img

    def handle_reference_images(self, character_reference_images, scene_index):
        print(colored('\n\nhandling reference images for final scenes', color='blue'))
        first_ref_img = character_reference_images[0] if len(character_reference_images) > 0 else None
        second_ref_img = character_reference_images[1] if len(character_reference_images) > 1 else first_ref_img
        return first_ref_img, second_ref_img

    def generate_final_scene_image(self, reference_canny_img, first_ref_img, second_ref_img, final_prompt, scene_index):
        print(colored('\n\ngenerating final scene image for final scenes', color='blue'))
        yield "text", False, "Checkingggggggggggggggggg"
        yield "text", False, final_prompt
        yield "file", True, reference_canny_img, "reference image for scene"
        yield "file", True, first_ref_img, "first reference image for scene"
        yield "file", True, second_ref_img, "second reference image for scene"
        image_data = SDAPI.reference_image(conditioned_image=reference_canny_img, first_ref_image=first_ref_img, second_ref_image=second_ref_img, prompt=final_prompt)
        self.db.scenes[scene_index].image = image_data
        with open(self.local_dir(f"final_scene{scene_index}.png"), "wb") as f:
            f.write(base64.b64decode(image_data))
        return image_data

        
    def save_db(self):
        with open(self.local_dir('db.json'), 'w') as f:
            f.write(self.db.model_dump_json(exclude_none=True))

    def sync_scenes_in_db(self, image, index):
        self.db.scenes[index].image = image
        self.save_db()
        print(f"-------- scene {index} synced ----------")
        
    def update_inpainted_image(self):
        print(colored('\n\nupdating inpainted image', color='blue'))
        
        yield "file", True, self.local_dir(f"final_scene0.png"),"final scene 0"
        yield "file", True, self.local_dir(f"final_scene1.png"),"final scene 1"
    
    
    