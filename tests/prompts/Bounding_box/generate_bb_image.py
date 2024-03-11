from PIL import Image
import ast
from unittest import TestCase
from dotenv import load_dotenv

load_dotenv()


def generate_bb_image(bounding_box, s):
            images = []
            dimensions = []
            bb_string = bounding_box
                # Load the images of the characters based on the file naming convention
            for box in bb_string:
                character = box["character"]
                file_path = f"tests/prompts/Bounding_box/object_detection/inputs/{character}_bb.png"  # Construct the file path
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
            final_image_path = f"tests/prompts/Bounding_box/object_detection/outputs/scene{s}_bounding_box.png" 
            canvas.save(final_image_path, "PNG")


class TestBoundingBoxImage(TestCase):
    def test_first_scene(self):
        bounding_box = [
{"character":"Bala","dimensions":[100, 360, 460, 600]},
{"character":"Simba","dimensions":[600, 480, 300, 480]}
]
        generate_bb_image(bounding_box=bounding_box, s=0)
        print("finished first scene")
        
    def test_second_scene(self):
        bounding_box = [
{"character":"Bala","dimensions":[100, 270, 410, 550]},
{"character":"Simba","dimensions":[520, 410, 300, 400]}
]
        generate_bb_image(bounding_box=bounding_box, s=1)
        print("finished second scene")
        
        
    # testing an old scene
    def test_old_scene(self):
        bounding_box = [
{"character":"Bala","dimensions" :[100, 260, 510, 600]},
{"character":"Simba","dimensions" :[650, 300, 470, 560]}
]
        generate_bb_image(bounding_box=bounding_box, s=2)
        print("finished old scene")
        

    
    def test_manual(self):
        bounding_box = [
{"character":"bala","dimensions" :[100, 260, 600, 700]},
{"character":"simba","dimensions" :[650, 300, 420, 500]}
]
        generate_bb_image(bounding_box=bounding_box, s=3)
        print("finished old scene")
        
    # test object detection scenario
    def test_OD_scenario_1(self):
        bounding_box = [
{"character":"Bala", "dimensions":[100, 400, 300, 560]},
{"character":"Simba", "dimensions":[650, 500, 250, 190]}
]
        generate_bb_image(bounding_box=bounding_box, s=4)
        print("finished old scene")
        

