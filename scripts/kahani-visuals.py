# IMPORTING LIBRARIES
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
import requests
import json
import re


#IMPORTING CLASSES
from visual_processor import VisualProcessor
from diffusionmodels import t2i_models

# LOADING ENVIRONMENT VARIABLES
load_dotenv(r"../.env")
managed_identity_client_id = os.environ.get("MANAGED_IDENTITY_CLIENT_ID")
openai_endpoint = os.environ.get("OPENAI_ENDPOINT")
openai_deployment_name = os.environ.get("OPENAI_DEPLOYED_MODEL")

# LINKS OR REFERENCES
# Pipeline flowcharts have been added here : https://microsoftapc-my.sharepoint.com/:p:/g/personal/t-dsudharsan_microsoft_com/Ed_8ZxXCvMRNrFcNWQ4X12wBDM3H-Ap7vf4Hbo5eF6ZK0A?e=IcmhMy


class visualprompts():

    def __init__(self):
        token_credential = DefaultAzureCredential(managed_identity_client_id=managed_identity_client_id)
        self.token = token_credential.get_token('https://cognitiveservices.azure.com/.default').token

    def read_gpt_prompt(self, prompt_dir):
        system_prompt_path = f"{prompt_dir}system_prompt.txt"
        user_prompt_path = f"{prompt_dir}user_prompt.txt"

        try:
            # Read system prompt from file
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()

            # Read user prompt template from file
            with open(user_prompt_path, 'r', encoding='utf-8') as f:
                user_prompt_template = f.read()

        except FileNotFoundError:
            print(f"Error: Prompt files not found in the 'prompts' directory.")
            system_prompt = ""
            user_prompt_template = ""

        return system_prompt, user_prompt_template

    def gpt4o_query(self,prompts):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        data = {
            'model': openai_deployment_name,
            'top_p': 0.5,
            'messages':[],
            'response_format': {
                'type': 'json_object'
            }
        }

        if prompts is not None:
            data["messages"] = prompts
            try:
                response = requests.post(openai_endpoint, headers=headers, data=json.dumps(data)) 
                response_json = response.json()
                # print("RESPONSE : ",response_json["choices"][0]["message"]["content"])
            except Exception as e:
                print("ERROR : ",e)
        return response_json["choices"][0]["message"]["content"]
    
    def scene_visuals_mapping(self,poses_dir):
        """Creates a dictionary such that each scene of each module contains the list of image paths of all 
        master visuals of characters in that scene."""

        module_scene_dict = {}

        for filename in os.listdir(poses_dir):
            match = re.match(r".*_module_(\d+)_scene_(\d+)\.png", filename)  # Match any filename
            if match:
                module_no = match.group(1)
                scene_no = match.group(2)

                if f"Module {module_no}" not in module_scene_dict:
                    module_scene_dict[f"Module {module_no}"] = {}
                if f"Scene {scene_no}" not in module_scene_dict[f"Module {module_no}"]:
                    module_scene_dict[f"Module {module_no}"][f"Scene {scene_no}"] = []

                module_scene_dict[f"Module {module_no}"][f"Scene {scene_no}"].append(os.path.join(poses_dir, filename))

        return module_scene_dict

    def sceneprompt_mastervisuals_mapping(self,json_file_path, module_scene_dict):
        """Crates a dictionary such that each scene of each module contains the prompt and 
        the list of image paths of all master visuals of characters in that scene."""

        with open(json_file_path, "r") as f:
            new_json_data = json.load(f)

        combined_data = {}

        for module_name, scenes in new_json_data.items():
            # module_num = module_name.split(" ")[1] #Extract module number
            if module_name in module_scene_dict:
                combined_data[module_name] = {}
                for scene_name, string_value in scenes.items():
                    # scene_num = scene_name.split(" ")[1] #Extract scene number
                    if scene_name in module_scene_dict[module_name]:
                        combined_data[module_name][scene_name] = {
                            "string": string_value,
                            "files": module_scene_dict[module_name][scene_name]
                        }
                    else:
                        print(f"Warning: Scene {scene_name} not found in module_scene_dict for {module_name}")
            else:
                print(f"Warning: Module {module_name} not found in module_scene_dict")

        return combined_data

# VARIABLES TO BE DEFINED
story_title = "ramesh"
modules = 5
scenes = 6

# CREATION OF CLASS OBJECTS
visualprocessor = VisualProcessor()
t2i_prompts = visualprompts()
models = t2i_models()

# I/O DIRECTORIES
## DATA DIRECTORY
data_dir = "../data/" # Directory where the data is stored

## OUTPUT DIRECTORIES
dir_loc = f"../outputs/{story_title}/" #MAIN OUTPUT DIRECTORY
os.makedirs(dir_loc,exist_ok=True)
dir_loc += story_title

#===========================================================================
# TODO Generate T2I prompts for each scene

with open(f"{data_dir}{story_title}/character_profiles.json", "r") as f:
    #read json data from file and store it in a variable as a string and pass inside prompt_templates as input
    input_character_profiles = json.load(f)

with open(f"{data_dir}{story_title}/scene_splitting.json", "r") as f:
    #read json data from file and store it in a variable as a string and pass inside prompt_templates as input
    input_stories = json.load(f)

t2i_prompt_dir = "../prompts/module_t2i_prompt_generation/"

t2i_prompts_list = {}

for module_data in input_stories["modules"]:
    module_number = module_data["module_number"]
    scene_data = module_data["scenes"]

    system_prompt, user_prompt_template = t2i_prompts.read_gpt_prompt(t2i_prompt_dir)
    user_prompt = user_prompt_template.format(input_scenes=str(scene_data),input_character_profiles=str(input_character_profiles))

    prompts = [{"role" : "system","content":[{"type":"text","text": system_prompt}]},
            {"role" : "user","content":[{"type":"text","text": user_prompt}]}]

    t2i_prompts_output = json.loads(t2i_prompts.gpt4o_query(prompts))
    t2i_prompts_list[f"Module {module_number}"] = t2i_prompts_output

    # with open(f'{dir_loc}_visual_prompt_planning_module{module_number}.json', 'w', encoding='utf-8') as f:
    #     json.dump(t2i_prompts_output, f, indent=4,ensure_ascii=False)
    #     print(f"Saving the generated prompts in {dir_loc}_visual_prompt_planning_module{module_number}.json")

with open(f'{dir_loc}_visual_prompt_planning.json', 'w', encoding='utf-8') as f:
        json.dump(t2i_prompts_list, f, indent=4,ensure_ascii=False)
        print(f"Saving the generated prompts in {dir_loc}_visual_prompt_planning.json")

#===========================================================================
# TODO Generate master character visuals for each character against a white background
## TODO Generate T2I prompts for generating the master character visuals for each character

# with open(f"{data_dir}{story_title}/character_profiles.json", "r") as f:
#     #read json data from file and store it in a variable as a string and pass inside prompt_templates as input
#     input_character_profiles = json.load(f)

char_t2i_prompt_dir = "../prompts/character_asset_generation/"

system_prompt, user_prompt_template = t2i_prompts.read_gpt_prompt(char_t2i_prompt_dir)
user_prompt = user_prompt_template.format(input_character_profiles=str(input_character_profiles))

prompts = [{"role" : "system","content":[{"type":"text","text": system_prompt}]},
        {"role" : "user","content":[{"type":"text","text": user_prompt}]}]

char_t2i_prompts_output = json.loads(t2i_prompts.gpt4o_query(prompts))

with open(f'{dir_loc}_character_prompts_list.json', 'w', encoding='utf-8') as f:
    json.dump(char_t2i_prompts_output, f, indent=4,ensure_ascii=False)
    print(f"Saving the generated prompts in {dir_loc}_character_prompts_list.json")

## TODO Generate the master visuals for each character using the above generated prompts
character_assets_dir = os.path.join(os.path.dirname(dir_loc), "images/character_assets/")
os.makedirs(character_assets_dir, exist_ok=True)

# with open(f'{dir_loc}_character_prompts_list.json', 'r') as f:
#     char_t2i_prompts_output = json.load(f)

for name, prompt in char_t2i_prompts_output.items():
    filename = name.replace(" ", "_") + ".png"  # Replace spaces and add .png extension
    filepath = os.path.join(character_assets_dir, filename) # Construct full file path
    models.flux_replicate(prompt,"",filepath)
    print(f"Generated image for character: '{name}' and saving to: {filepath}")

## TODO Evaluate the master character visuals that were generated
character_eval_dir = "../prompts/character_asset_eval/"

feedback_list = {}
for name, prompt in char_t2i_prompts_output.items():
    original_filepath = os.path.join(character_assets_dir, name.replace(" ", "_") + ".png")
    filepath = os.path.join(character_assets_dir, name.replace(" ", "_") + "_refined.png")
    master_character_visual_uri = visualprocessor.encode_image_to_data_uri(original_filepath)
    for character in input_character_profiles["character_profiles"]:
        if character["name"] == name:
            input_profile = character
    
    system_prompt, user_prompt_template = t2i_prompts.read_gpt_prompt(character_eval_dir)
    user_prompt = user_prompt_template.format(input_profile = str(input_profile), prompt = prompt)

    prompts = [
                {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
                {"role": "user", "content": [{"type": "text", "text": user_prompt}, {"type": "image_url", "image_url": {"url": master_character_visual_uri}}]}
            ]

    feedback_output = json.loads(t2i_prompts.gpt4o_query(prompts))
    print("===========================================")
    # print(feedback_output)
    feedback_list[name] = feedback_output

    models.flux_replicate(feedback_output["Prompt"],master_character_visual_uri,filepath)
    print(f"Generated REFINED master character visual image for character: '{name}' and saving to: {filepath}")

with open(f'{dir_loc}_character_prompts_feedback.json', 'w', encoding='utf-8') as f:
    json.dump(feedback_list, f, indent=4,ensure_ascii=False)
    print(f"Saving the generated prompts feedback in {dir_loc}_character_prompts_feedback.json")

## TODO Segregating T2I prompts for each character in each scene
poses_dir = os.path.join(os.path.dirname(dir_loc), "images/poses/")
os.makedirs(poses_dir, exist_ok=True)

scene_reference_prompt_dir = "../prompts/scene_references_gen/"

with open(f'{dir_loc}_visual_prompt_planning.json', 'r') as f:
        json_data = json.load(f)

system_prompt, user_prompt_template = t2i_prompts.read_gpt_prompt(scene_reference_prompt_dir)
user_prompt = user_prompt_template.format(input_prompts_list=str(json_data))
prompts = [{"role" : "system","content":[{"type":"text","text": system_prompt}]},
        {"role" : "user","content":[{"type":"text","text": user_prompt}]}]

scene_reference_prompts_output = json.loads(t2i_prompts.gpt4o_query(prompts))
with open(f'{dir_loc}_scene_reference_prompts.json', 'w', encoding='utf-8') as f:
    json.dump(scene_reference_prompts_output, f, indent=4,ensure_ascii=False)
    print(f"Saving the generated prompts in {dir_loc}_scene_reference_prompts.json")

# NOTE TODO ABOVE NEED TO BE WORKED BECAUSE SCENE REFERENCE PROMPTS GIVING ONLY FOR ONE MODULE ATM

## TODO Based on the scene-wise character prompts, generate the visuals for each character in each scene as master visual

with open(f'{dir_loc}_scene_reference_prompts.json', 'r') as f:
    json_data = json.load(f)

for module_name, scenes in json_data.items():
    module_num = module_name.split(" ")[1]
    for scene_name, characters in scenes.items():  # Iterate through characters in the scene
        scene_num = scene_name.split(" ")[1]
        for character_name, prompt in characters.items():
            character_asset_file = os.path.join(character_assets_dir, f"{character_name.replace(' ', '_')}_refined.png")

            if os.path.exists(character_asset_file):
                reference_uri = visualprocessor.encode_image_to_data_uri(character_asset_file)
                base_name = os.path.basename(character_asset_file).replace("_refined.png","")
                output_path = os.path.join(poses_dir, f"{base_name}_module_{module_num}_scene_{scene_num}.png")
                models.flux_replicate(prompt, reference_uri, output_path)
            else:
                print(f"Warning: Character asset not found for {character_name}")

## NOTE TODO Evaluation of the above pose visuals especially distortions, multiple characters, pose etc needs to be handled.
## NOTE TODO CONTINUED... even location related elements need to be checked and corrected

# TODO Generate the visuals for each scene with these reference per-scene character visuals
scene_images_dir = os.path.join(os.path.dirname(dir_loc), "images/scenes/")
os.makedirs(scene_images_dir, exist_ok=True)

result_dict = t2i_prompts.scene_visuals_mapping(poses_dir)

json_file_path = f"{dir_loc}_visual_prompt_planning.json"  # Path to your new JSON file
combined_data = t2i_prompts.sceneprompt_mastervisuals_mapping(json_file_path, result_dict)

for module, scene in combined_data.items():
    for scene_name, data in scene.items():
        module_no = module.replace(" ", "_").lower()
        scene_no = scene_name.replace(" ", "_").lower()
        combined_reference_uri = visualprocessor.combine_images(data['files'],f"{scene_images_dir}chars_{module_no}_{scene_no}.png")
        print(f"Combined Master Visuals of {module_no} {scene_no} saved in : {scene_images_dir}chars_{module_no}_{scene_no}.png")
        models.flux_replicate(data['string'], combined_reference_uri, f"{scene_images_dir}{module_no}_{scene_no}_visuals.png")
        print("==============================================")
    print("==============================================")

# NOTE TODO One more evaluation need to be in place here for count of characters but mostly prompt template alignment
# in general

# NOTE TODO Image grid and how we want the grid to be and/or narration overlays


# # Generate visuals
# models = t2i_models()
# flux_images = []
# flux_images_wn = []
# visual_prompts_list = list(t2i_prompts_output.values())

# images_dir = os.path.join(os.path.dirname(dir_loc), "images/")
# os.makedirs(images_dir, exist_ok=True)

# row_number = 1
# column_number = 0
# current_row_limit = display_columns[row_number - 1]
# index = 0
# narrations = list(scenes_list.values())
# for prompt in visual_prompts_list:
#     flux_output = models.flux_t2i(prompt)
#     # Calculate row and column numbers
#     column_number += 1
#     if column_number > current_row_limit:  # End of the current row
#         row_number += 1
#         column_number = 1
#         current_row_limit = display_columns[row_number - 1] 

#     # Save individual output with naming convention
#     file_name = f"{images_dir}{story_title}_scene_{index+1}.png"
#     flux_output.save(file_name) 
#     flux_images.append(flux_output)
#     print(f"Saving the individual generated scene in {file_name}")
#     flux_output_wn = scenes.add_text_with_box(file_name, narrations[index], f"{images_dir}{story_title}_module_{row_number}_scene_{column_number}_wn.png")
#     flux_images_wn.append(flux_output_wn)
#     index += 1
#     print(f"Saving the individual generated scene with narration in {images_dir}{story_title}_module_{row_number}_scene_{column_number}_wn.png")

# flux_visual_grid = scenes.image_grid(flux_images, rows=display_rows, cols_per_row=display_columns)
# # Save the grid image
# flux_visual_grid.save(f'{dir_loc}_flux_visuals.png')
# print(f"Saving the generated visuals image grid in {dir_loc}_flux_visuals.png")

# flux_visual_grid_wn = scenes.image_grid(flux_images_wn, rows=display_rows, cols_per_row=display_columns)
# # Save the grid image
# flux_visual_grid_wn.save(f'{dir_loc}_flux_visuals_wn.png')
# print(f"Saving the generated visuals image grid in {dir_loc}_flux_visuals_wn.png")
# print("================================ SUCCESSFULLY GENERATED VISUALS ====================================")
