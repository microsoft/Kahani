import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import base64
from pathlib import Path

class VisualProcessor:
    def __init__(self):
        pass

    def get_scenes(self, data):
        narrations = {}
        cnt = 0
        grid_rows = len(data["modules"])
        grid_cols = []
        for module in data["modules"]:
            grid_cols.append(len(module["scenes"]))
            for scenes in module["scenes"]:
                cnt +=1
                narrations[f"Scene {cnt}"] = scenes["description"]
        return grid_rows, grid_cols, narrations

    def load_data(self, input_file):
        with open(input_file, 'r') as f:
            data = json.load(f)
        return data

    def get_scene_grid_layout(self, input_file):
        data = self.load_data(input_file)
        return self.get_scenes(data)

    def image_grid(self,imgs, rows, cols_per_row):
        total_images = sum(cols_per_row)
        assert len(imgs) <= total_images  # Ensure enough images for all rows

        w, h = imgs[0].size
        placeholder = Image.open("../data/placeholder_image.jpg")
        placeholder = placeholder.resize((w, h))  # Resize placeholder to match image size

        grid_width = max(cols * w for cols in cols_per_row)
        grid_height = rows * h
        grid = Image.new('RGB', size=(grid_width, grid_height))

        start_col = 0
        for row_index in range(rows):
            cols = cols_per_row[row_index]
            for col_index in range(cols):
                if col_index < len(imgs):
                    img_index = start_col + col_index
                    grid.paste(imgs[img_index], box=(col_index * w, row_index * h))
                else:
                    grid.paste(placeholder, box=(col_index * w, row_index * h))
            start_col += cols

        return grid
    
    def get_max_font_size(self,text, box_width, box_height, font_path):
        """Calculate maximum font size that fits within the box dimensions."""
        # Start with a reasonably large font size
        font_size = 100
        
        # Load the font (you can adjust the initial font size here)
        font = ImageFont.truetype(font_path, font_size)
        img = Image.new('RGB', (box_width, box_height), (255, 255, 255))  # Dummy image to calculate size
        draw = ImageDraw.Draw(img)
        
        # Wrap the text
        wrapped_text = textwrap.fill(text, width=40)  # Wrapping text to a max of 20 chars per line
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)  # Get the bounding box of the text
        text_width = text_bbox[2] - text_bbox[0]  # text_bbox returns (left, top, right, bottom)
        text_height = text_bbox[3] - text_bbox[1]

        # Adjust font size until the text fits inside the box
        while text_width > box_width or text_height > box_height:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        
        return font_size

    def add_text_with_box(self,image_path, text, output_path):
        # Open the image
        img = Image.open(image_path)
        font_path="/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        width, height = img.size

        # Define the height of the translucent box (1/4th of the image height)
        box_height = height // 4
        box_top = height - box_height

        # Create a semi-transparent overlay
        box = Image.new('RGBA', (width, box_height), (0, 0, 0, 128))  # (R, G, B, A) for transparency
        img.paste(box, (0, box_top), box)  # Paste the box onto the image

        # Get the maximum font size that fits within the box dimensions
        font_size = self.get_max_font_size(text, width, box_height, font_path)
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(img)

        # Wrap the text
        wrapped_text = textwrap.fill(text, width=40)  # Adjust text wrapping as needed

        # Calculate text position
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)  # Get the bounding box of the text
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Center the text in the box
        text_x = (width - text_width) // 2
        text_y = box_top + (box_height - text_height) // 2

        # Add the wrapped text on the box
        draw.text((text_x, text_y), wrapped_text, fill=(255, 255, 255), font=font)

        # Save the resulting image
        img.save(output_path)
        return img
    
    def encode_image_to_data_uri(self,image_path):
        """
        Encodes an image to a Base64 data URI.
        Args:
            image_path (str): Path to the image file.
        
        Returns:
            str: Base64 data URI of the image.
        """
        if not Path(image_path).is_file():
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        
        mime_type = "image/" + Path(image_path).suffix.lstrip(".").lower()  # Infer MIME type from file extension
        with open(image_path, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:{mime_type};base64,{base64_string}"
        
    def combine_images(self, character_scene_images,output_path):
        # Combine images horizontally
        width = 0
        width_location = [0]
        height = 0
        images = []
        for img_path in character_scene_images:
            img = Image.open(img_path)
            width += img.width
            width_location.append(width)
            height = max(height, img.height)
            images.append(img)

        # img1 = Image.open(character_scene_images[0])
        # img2 = Image.open(character_scene_images[1])
        composite = Image.new("RGB", (width, height))
        # composite = Image.new("RGB", (img1.width + img2.width, max(img1.height, img2.height)))
        for index in range(len(images)):
            # if index == 0:
            #     composite.paste(images[index], (width_location[index], 0))
            # else:
            composite.paste(images[index], (width_location[index], 0))
        # composite.paste(img1, (0, 0))
        # composite.paste(img2, (img1.width, 0))
        composite.save(output_path)
        # image_prompt = self.encode_image_to_data_uri(output_path)
        # print(image_prompt[:100])
        # Use the combined image
        with open(output_path, "rb") as file:
            data = base64.b64encode(file.read()).decode("utf-8")
            image_prompt = f"data:application/octet-stream;base64,{data}"

        return image_prompt
