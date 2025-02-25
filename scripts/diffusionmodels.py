import torch
from diffusers import FluxPipeline,FluxTransformer2DModel
from huggingface_hub import login
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from torchao.quantization import quantize_, int8_weight_only
import torch
from sd_embed.embedding_funcs import get_weighted_text_embeddings_flux1
import gc
from azure.identity import DefaultAzureCredential
import requests
import replicate

# https://www.analyticsvidhya.com/blog/2024/06/stable-diffusion-3/
# Above documentation has with and without GPU and also mem optimizations

# load the tokens and keys

# Control net resources in case we are planning to do
# SD3- https://huggingface.co/docs/diffusers/main/en/api/pipelines/controlnet_sd3
# Flux - https://huggingface.co/docs/diffusers/main/en/api/pipelines/controlnet_flux

# https://blackforestlabs.ai/flux-1-tools/

# References
# https://medium.com/@natsunoyuki/using-long-prompts-with-the-diffusers-package-with-prompt-embeddings-819657943050
# https://github.com/huggingface/diffusers/issues/2136#issuecomment-1514338525
# TODO: FOR EMBEDDINGS (ADD TO REQUIREMENTS.TXT LATER)
#https://github.com/xhinker/sd_embed?tab=readme-ov-file (they have citation)
# pip install torchao --extra-index-url https://download.pytorch.org/whl/cu121
# pip install git+https://github.com/xhinker/sd_embed.git@main

load_dotenv(r"../.env")
HF_TOKEN = os.environ.get("HF_TOKEN")
login(token=HF_TOKEN)
managed_identity_client_id = os.environ.get("MANAGED_IDENTITY_CLIENT_ID")
dalle3_endpoint = os.environ.get("DALLE3_OPENAI_ENDPOINT")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

class t2i_models():
    def __init__(self):

        #DALLE3
        token_credential = DefaultAzureCredential(managed_identity_client_id=managed_identity_client_id)
        self.token = token_credential.get_token('https://cognitiveservices.azure.com/.default').token

        #DEFAULT PLACEHOLDER IMAGE IN CASE OF ERRORS
        self.placeholder_image = Image.open(r"../data/placeholder_image.jpg")

    def flux_pulid(self,prompt,image_prompt,output_path):
        replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        model = "bytedance/flux-pulid:8baa7ef2255075b46f4d91cd238c21d31181b3e6a864463f967960bb0112525b"

        output = output = replicate_client.run(
            model,
            input={
                "width": 896,
                "height": 1152,
                "prompt": prompt,
                "true_cfg": 1,
                "id_weight": 1,
                "num_steps": 20,
                "start_step": 4,
                "num_outputs": 1,
                "output_format": "png",
                "guidance_scale": 4,
                "output_quality": 80,
                "main_face_image": image_prompt,
                "negative_prompt": "bad quality, worst quality, text, signature, watermark, extra limbs",
                "max_sequence_length": 128
            }
        )   
        response = requests.get(output[0], stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        image = Image.open(BytesIO(response.content))  # Open the image using PIL
        image.save(output_path)  # Save the image to the specified path
        print(f"Image saved to: {output_path}")

    def flux_fofd(self,prompt,image_prompt,output_path):
        model = "fofr/consistent-character:9c77a3c2f884193fcee4d89645f02a0b9def9434f9e03cb98460456b831c8772"
        replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

        output = replicate_client.run(
            model,
            input={
                "prompt": prompt,
                "subject": image_prompt,
                "output_format": "png",
                "output_quality": 80,
                "negative_prompt": "Change in style, change in culture, distorted images",
                "randomise_poses": False,
                "number_of_outputs": 1,
                "number_of_images_per_pose": 1
            }
        )
        print(output)
        response = requests.get(output, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        image = Image.open(BytesIO(response.content))  # Open the image using PIL
        image.save(output_path)  # Save the image to the specified path
        print(f"Image saved to: {output_path}")


        # The fofr/consistent-character model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        # for item in output:
        #     # https://replicate.com/fofr/consistent-character/api#output-schema
        #     print(item)


    def flux_replicate(self,prompt,image_prompt,output_path):
        # with open(image_path, "rb") as file:
        #     data = base64.b64encode(file.read()).decode("utf-8")
        #     image_prompt = f"data:application/octet-stream;base64,{data}"

        replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)
        model = "black-forest-labs/flux-1.1-pro-ultra"
        # model = "black-forest-labs/flux-dev"

        if image_prompt == "":
            output = replicate_client.run(model, input={"prompt": prompt,
                                                    "output_format":"png",
                                                    "seed":1234
                                                    }
                                    )
        else:
            output = replicate_client.run(model, input={"prompt": prompt,
                                                        "image_prompt": image_prompt,
                                                        "image_prompt_strength": 0.8,
                                                        "output_format":"png",
                                                        "seed":1234
                                                        }
                                        )

        # image_name = f"module_{module_id}_scene_{scene_id}.png"
        # # Initialize the image path (note the filetype should be png)
        # image_path = os.path.join(scenes_folder_path, image_name)
        # print(output)
        # for index, item in enumerate(output):
        #     with open(output_path, "wb") as file:
        #         print("INDEXXX",index)
        #         file.write(item.read())

        with open(output_path, "wb") as file:
            file.write(output.read())
            print(f"Image saved at {output_path}")
    
    # TEXT2IMAGE FUNCTIONS
    
    # LONG PROMPT HANDLING USING EMBEDDINGS - T2I
    def flux_t2i(self, prompt):
        print("===================================== FLUX")
        model_path = "black-forest-labs/FLUX.1-dev"

        transformer = FluxTransformer2DModel.from_pretrained(
            model_path, subfolder = "transformer", torch_dtype = torch.bfloat16,cache_dir="../../.cache/huggingface/hub"
        )
        quantize_(transformer, int8_weight_only())

        pipe = FluxPipeline.from_pretrained(
            model_path, transformer = transformer, torch_dtype = torch.bfloat16, cache_dir="../../.cache/huggingface/hub"
        )

        pipe.to('cuda')
        # pipe.enable_model_cpu_offload()

        prompt_embeds, pooled_prompt_embeds = get_weighted_text_embeddings_flux1(pipe = pipe, prompt = prompt)

        image = pipe(
            prompt_embeds               = prompt_embeds
            , pooled_prompt_embeds      = pooled_prompt_embeds
            , width                     = 1024
            , height                    = 1024
            , num_inference_steps       = 50
            , guidance_scale            = 7.0
            , generator                 = torch.Generator().manual_seed(1234)
        ).images[0]

        del prompt_embeds,pooled_prompt_embeds
        # pipe.to('cpu')
        gc.collect()
        torch.cuda.empty_cache()
        return image