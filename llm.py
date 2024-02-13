import base64
import json
import os
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import urllib.parse


# @retry(wait=wait_random_exponential(
#     multiplier=10,
#     max=120),
    # stop=stop_after_attempt(5))
def llm(messages, **kwargs):
    client = openai.Client(
        api_key=os.environ["OPENAI_API_KEY"],
    )
    kwargs['model'] = kwargs.get('model', 'gpt-4-1106-preview')
    kwargs['messages'] = messages
    args = {k: v for k, v in kwargs.items() if k in [
        'model', 'messages', 'temperature', 'tools', 'stream']}

    completions = client.chat.completions.create(
        **args
    )

    if args.get('stream', False):
        # full_response = ""
        for chunk in completions:
            for choice in chunk.choices:
                if choice.finish_reason == 'stop':
                    break
                if choice.delta.content is not None:
                    yield choice.delta.content
                    # full_response += choice.delta.content
        # return full_response
    elif args.get('tools', None) is None:
        return completions.choices[0].message.content
    else:
        fn = completions.choices[0].message.tool_calls[0].function
        return {
            'function': fn.name,
            'arguments': json.loads(fn.arguments)
        }


def llm_vision(imgs, isGoogle=False, description="", count=4):
    if isGoogle:
        img_comp_msg = comp_imgs(imgs, True, description, count)
    else:
        img_comp_msg = comp_imgs(imgs)
    
    client = openai.Client(
        api_key=os.environ["OPENAI_API_KEY"],
    )
    completions = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[img_comp_msg],
    )
    print(completions.choices[0])
    return completions.choices[0].message.content


def sm(prompt):
    return {'role': 'system', 'content': prompt}


def um(prompt):
    return {'role': 'user', 'content': prompt}


def comp_imgs(imgs, isGoogle=False, description="", count=4):
    content = []
    if isGoogle:
        e1 = {
        "type": "text",
        "text": f'I am providing you with {count} images. Which of the images matches the best with the description: {description}.\nYOU JST HAVE TO CHOOSE THE BEST IMAGE AND TELL ME WHICH IMAGE IT IS, 1-{count}. Do NOT give reason for your choice, JUST GIVE THE NUMBER of your chosen image.'
    }
    else:
        e1 = {
            "type": "text",
            "text": f'I want to select a picture to include in a storybook. Some of the images are not well structured, and have some inconsistencies. Select the best image out of the {count} based on clarity. You always have to choose one of the images. Do NOT give reason for your choice, JUST GIVE THE NUMBER of your chosen image.'
        }
    content.append(e1)
    for img in imgs:
        e = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img}"
            }
        }
        content.append(e)

    return um(content)


def fn(name, description, params, required):
    return {
        'type': 'function',
        'function': {
            'name': name,
            'description': description,
            'parameters': {
                'type': 'object',
                'properties': {k: v for k, v in params.items()},
                'required': required
            }
        }
    }


def get_image_urls(query, num_images):
    image_urls = []
    index = 0
    while len(image_urls) < num_images:
        index += 1
        search_query = query + ' images'
        search_results = search(search_query, num=num_images*index, stop=num_images*index, pause=2)

        for url in search_results:
            if 'googleusercontent' in url:
                continue
            try:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                for img in soup.find_all('img'):
                    img_url = img.get('src')
                    if img_url and img_url.startswith('http'):
                        if img_url.split('.')[-1] == 'png' or img_url.split('.')[-1] == 'jpg' or img_url.split('.')[-1] == 'jpeg':
                            image_urls.append(img_url)
                            if len(image_urls) >= num_images:
                                for url in image_urls:
                                    print(url)
                                return image_urls
            except Exception as e:
                print(f"Error processing {url}: {e}")

    return image_urls[:num_images]

def download_images(image_urls):
    img_exts = []
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            image_type = url.split('.')[-1]
            if not image_type:
                image_type = "jpg"
            img_exts.append(image_type)
            with open(f"google_image_{i+1}.{image_type}", 'wb') as f:
                f.write(response.content)
            print(f"Image {i+1} downloaded")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")
    return img_exts

def get_best_img(prompt):
    num_images = 4  
    image_urls = get_image_urls(prompt, num_images)
    img_exts = download_images(image_urls)
    
    base64_imgs = []

    for i in range(num_images):
        index = i+1
        with open(f'./google_image_{index}.{img_exts[i]}', 'rb') as img_file:
            img_data = img_file.read()
            base64_imgs.append(base64.b64encode(img_data).decode("utf-8"))
    
    return(llm_vision(base64_imgs, True, prompt, num_images))


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    result = llm([
        sm("Respond by using functions only"),
        um("The story needs to have a good ending")
    ], tools=[
        fn('update_story', 'Update the current story', {'change': {
            'type': 'string', 'description': 'instructions from the user'}}, ['change']),
        fn('update_characters', 'Update the characters in the story', {'change': {
            'type': 'string', 'description': 'instructions from the user'}}, ['change']),
        fn('update_scenes', 'Update the scenes in the story', {'scene_number': {
            'type': 'integer', 'description': 'scene number'},
            'change': {
            'type': 'string', 'description': 'instructions from the user'}}, ['change']),
    ])

    print(result)
