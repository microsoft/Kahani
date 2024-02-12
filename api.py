from PIL import Image
import argparse
import base64
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()


HOST = os.environ.get("SDAPI_HOST")
STANDARD_WIDTH = 1280
STANDARD_HEIGHT = 960
NEGATIVE_PROMPT ="EasyNegative, blurry, (bad_prompt:0.8), (artist name, signature, watermark:1.4), (ugly:1.2), (worst quality, poor detail:1.4), (deformed iris, deformed pupils, semi-realistic, CGI, 3d, render, sketch, drawing, anime:1.4), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, lowres, error, worst quality, low quality, out of frame, username, NSFW"


class SDAPI:

    def text2image(**kwargs):

        if "width" not in kwargs:
            kwargs["width"] = STANDARD_WIDTH

        if "height" not in kwargs:
            kwargs["height"] = STANDARD_HEIGHT

        if "seed" not in kwargs:
            kwargs["seed"] = -1

        if "steps" not in kwargs:
            kwargs["steps"] = 40

        # kwargs['sd_model_hash'] = "31e35c80fc"
        kwargs['sd_model_name'] = "sd_xl_base_1.0"
        kwargs['sampler_name'] = "DPM++ 2M Karras"
        # kwargs['sd_vae_hash'] = None
        # kwargs['sd_vae_name'] = "sdxl_vae"
        kwargs['refiner_checkpoint'] = "sd_xl_refiner_1.0.safetensors"
        kwargs['refiner_switch_at'] = 0.8
        kwargs['negative_prompt'] = NEGATIVE_PROMPT
        

        print("text2image API sent to server")
        response = requests.post(HOST + "/sdapi/v1/txt2img", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            info = body['info']
            print(json.loads(info))
            return body['images'][0]
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def image2image(**kwargs):
        isInpainting = False
        if "width" not in kwargs:
            kwargs["width"] = STANDARD_WIDTH

        if "height" not in kwargs:
            kwargs["height"] = STANDARD_HEIGHT

        if "seed" not in kwargs:
            kwargs["seed"] = -1

        if "steps" not in kwargs:
            kwargs["steps"] = 40

        if "mask_blur" not in kwargs:
            kwargs["mask_blur"] = 4

        if "inpaint_full_res_padding" not in kwargs:
            kwargs["inpaint_full_res_padding"] = 32

            # with open("inpaint_test.png", "rb") as f:
            #     img_data = f.read()
            #     img_data = base64.b64encode(img_data).decode("utf-8")
            #     kwargs['init_images'] = [img_data]

        with Image.open("./mask_api.png") as img:
            resized_img = img.resize((STANDARD_WIDTH, STANDARD_HEIGHT))
            resized_img.save("./mask_api.png")

        with open("mask_api.png", "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            kwargs['mask'] = img_data

        kwargs['sampler_index'] = "DPM++ 2M Karras"
        kwargs['negative_prompt'] = NEGATIVE_PROMPT


        print("image2image")

        response = requests.post(HOST + "/sdapi/v1/img2img", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            info = body['info']
            print(json.loads(info))
            if "batch_size" not in kwargs:
                return body['images'][0]
            return body['images']
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def controlnet(**kwargs):

        payload = {
            "controlnet_module": "canny",
            "controlnet_input_images": [kwargs['init_images'][0]],
            "controlnet_processor_res": 512,
            "controlnet_threshold_a": 64,
            "controlnet_threshold_b": 64
        }

        print("controlnet")

        response = requests.post(HOST + "/controlnet/detect", json=payload)
        if response.status_code == 200:
            body = response.json()
            return body['images'][0]
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def reference_guided_inpainting(**kwargs):
        if "width" not in kwargs:
            kwargs["width"] = 800

        if "height" not in kwargs:
            kwargs["height"] = 600

        if "seed" not in kwargs:
            kwargs["seed"] = -1

        if "steps" not in kwargs:
            kwargs["steps"] = 40

        if "mask_blur" not in kwargs:
            kwargs["mask_blur"] = 4

        if "inpaint_full_res_padding" not in kwargs:
            kwargs["inpaint_full_res_padding"] = 32

        if "denoising_strength" not in kwargs:
            kwargs["denoising_strength"] = 0.75

        if "mask" not in kwargs:
            raise ValueError("Mask is required for reference guided inpainting")


        if "ref" not in kwargs:
            raise ValueError("Reference image is required for reference guided inpainting")
        else:
            img_data = kwargs['ref']
        
        kwargs['negative_prompt'] = NEGATIVE_PROMPT
        kwargs['alwayson_scripts'] = {}
        kwargs['alwayson_scripts']['controlnet'] = {}
        kwargs['alwayson_scripts']['controlnet']['args'] = [
            {
                "enabled": True,
                "module": "reference_only",
                "model": "none",
                "weight": 1.0,
                "image": img_data,
                "resize_mode": 0,
                "lowvram": False,
                "control_mode": 0,
                "pixel_perfect": True
            }
        ]

        kwargs['sampler_index'] = "DPM++ 2M Karras"

        print("reference guided inpainting")

        response = requests.post(HOST + "/sdapi/v1/img2img", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            info = body['info']
            print(json.loads(info))
            return body['images']
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def remove_background(image, **kwargs):
        
        defaults = {
            "input_image": image,
            "model": "u2net",
            "return_mask": False,
            "alpha_matting": False,
            "alpha_matting_foreground_threshold": 240,
            "alpha_matting_background_threshold": 10,
            "alpha_matting_erode_size": 10
        }

        for k, v in kwargs.items():
            if k in ['input_image', 'model', 'return_mask', 'alpha_matting', 'alpha_matting_foreground_threshold', 'alpha_matting_background_threshold', 'alpha_matting_erode_size']:
                defaults[k] = v


        print("remove_background")
        response = requests.post(HOST + "/rembg", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            return body['image']
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

    def reference_image(conditioned_image,first_ref_image, second_ref_image, **kwargs):

        if "width" not in kwargs:
            kwargs["width"] = STANDARD_WIDTH

        if "height" not in kwargs:
            kwargs["height"] = STANDARD_HEIGHT

        if "seed" not in kwargs:
            kwargs["seed"] = -1

        if "steps" not in kwargs:
            kwargs["steps"] = 40

        # kwargs['sd_model_hash'] = "31e35c80fc"
        kwargs['sd_model_name'] = "sd_xl_base_1.0"
        kwargs['sampler_name'] = "DPM++ 2M Karras"
        kwargs['negative_prompt'] = NEGATIVE_PROMPT


        # kwargs['sd_vae_hash'] = None
        # kwargs['sd_vae_name'] = "sdxl_vae"
        kwargs['refiner_checkpoint'] = "7440042bbd"
        kwargs['refiner_switch_at'] = 0.8
        kwargs['alwayson_scripts'] = {}
        kwargs['alwayson_scripts']['controlnet'] = {}
        kwargs['alwayson_scripts']['controlnet']['args'] = [
            {
                "enabled": True,
                "module": "none",
                "model": "diffusers_xl_canny_full [2b69fca4]",
                "weight": 1,
                "preprocessor": "None",
                "image": conditioned_image,
                "resize_mode": "Just Resize",
                "lowvram": False,
                "guidance_start": 0.0,
                "guidance_end": 1.0,
                "control_mode": "Balanced",
                "pixel_perfect": True,
                "save_detected_map": True,
            },
            {
                "enabled": True,
                "module": "reference_only",
                "model": "none",
                "weight": 1,
                "preprocessor": "None",
                "image": first_ref_image,
                "resize_mode": "Just Resize",
                "lowvram": False,
                "threshold_a": 0.5,
                "guidance_start": 0.0,
                "guidance_end": 1.0,
                "control_mode": "Balanced",
                "pixel_perfect": False,
                "save_detected_map": True,
            },
            {
                "enabled": True,
                "module": "reference_only",
                "model": "none",
                "weight": 1,
                "preprocessor": "None",
                "image": second_ref_image,
                "resize_mode": "Just Resize",
                "lowvram": False,
                "threshold_a": 0.5,
                "guidance_start": 0.0,
                "guidance_end": 1.0,
                "control_mode": "Balanced",
                "pixel_perfect": False,
                "save_detected_map": True,
            }
        ]

        response = requests.post(HOST + "/sdapi/v1/txt2img", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            info = body['info']
            print(json.loads(info))
            return body['images'][0]
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None
    
    def pose_generation(reference_image, **kwargs):
 
        if "width" not in kwargs:
            kwargs["width"] = STANDARD_WIDTH
 
        if "height" not in kwargs:
            kwargs["height"] = STANDARD_HEIGHT
 
        if "seed" not in kwargs:
            kwargs["seed"] = -1
 
        if "steps" not in kwargs:
            kwargs["steps"] = 40
 
        # kwargs['sd_model_hash'] = "31e35c80fc"
        kwargs['sd_model_name'] = "sd_xl_base_1.0"
        kwargs['sampler_name'] = "DPM++ 2M Karras"
        kwargs['negative_prompt'] = NEGATIVE_PROMPT
 
 
        # kwargs['sd_vae_hash'] = None
        # kwargs['sd_vae_name'] = "sdxl_vae"
        kwargs['refiner_checkpoint'] = "sd_xl_refiner_1.0.safetensors"
        kwargs['refiner_switch_at'] = 0.8
        kwargs['alwayson_scripts'] = {}
        kwargs['alwayson_scripts']['controlnet'] = {}
        kwargs['alwayson_scripts']['controlnet']['args'] = [
            {
                "enabled": True,
                "weight": 1.0,
                "preprocessor": "reference_only",
                "image": reference_image,
                "resize_mode": 0,
                "lowvram": False,
                "guidance_start": 0.0,
                "guidance_end": 1.0,
                "control_mode": 0,
                "pixel_perfect": True,
            }
        ]
        response = requests.post(HOST + "/sdapi/v1/txt2img", json=kwargs)
        if response.status_code == 200:
            body = response.json()
            info = body['info']
            print(json.loads(info))
            return body['images'][0]
        else:
            print(
                f"[-] Failed to generate image. Status code: {response.status_code}")
            print(response.text)
            return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--action", type=str,
                           help="action: t2i or i2i", required=True)
    argparser.add_argument("--prompt", type=str,
                           help="prompt for the image", required=True)
    argparser.add_argument("--seed", type=int,
                           help="seed for image generation", required=False)
    argparser.add_argument("--steps", type=int,
                           help="steps for image generation", required=False)

    args = argparser.parse_args()

    if args.action == "t2i":

        kwargs = {k: v for k, v in vars(
            args).items() if v is not None and k != "action"}

        img_data = SDAPI.text2image(**kwargs)

        if img_data:
            img_data = base64.b64decode(img_data)

            with open("out.png", "wb") as f:
                f.write(img_data)

        else:
            print("Error generating image")

    elif args.action == "i2i":

        kwargs = {k: v for k, v in vars(
            args).items() if v is not None and k != "action"}

        with open("out.png", "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            kwargs['init_images'] = [img_data]

        img_data = SDAPI.image2image(**kwargs)

        if img_data:
            img_data = base64.b64decode(img_data)

            with open("out-refined.png", "wb") as f:
                f.write(img_data)

        else:
            print("Error generating image")

    elif args.action == "canny":

        kwargs = {k: v for k, v in vars(
            args).items() if v is not None and k != "action"}

        with open("out.png", "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            kwargs['init_images'] = [img_data]

        img_data = SDAPI.controlnet(**kwargs)

        if img_data:
            img_data = base64.b64decode(img_data)

            with open("out-canny.png", "wb") as f:
                f.write(img_data)

        else:
            print("Error generating image")

    elif args.action == "reference":

        kwargs = {k: v for k, v in vars(
            args).items() if v is not None and k != "action"}

        with open("inpaint_test.png", "rb") as f:
            img_data = f.read()
            img_data = base64.b64encode(img_data).decode("utf-8")
            kwargs['init_images'] = [img_data]

        img_data = SDAPI.reference_guided_inpainting(**kwargs)

        if img_data:
            img_data = base64.b64decode(img_data)

            with open("out-referenceInpainting.png", "wb") as f:
                f.write(img_data)

        else:
            print("Error generating image")

    else:
        print("Invalid action")

    