from PIL import Image
import numpy as np

img = Image.open("/home/deepikakhullar/YehHaiMeriKahani/tests/image_processing/inputs/bala_pose_one.png")
# pil image to numpy
img = np.array(img)
# unique pixel values from the numpy array
# print(numpy.unique(img, return_counts=True))
print(img.shape)
non_zero_coords = np.argwhere(img != 0)

# Get the bounding box coordinates
top_left = non_zero_coords.min(axis=0)
bottom_right = non_zero_coords.max(axis=0)

# Extract the part of the image within the bounding box
extracted_image = img[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]
print(extracted_image.shape)
# read image from numpy 
img = Image.fromarray(extracted_image)
# write img into a png file
img.save("/home/deepikakhullar/YehHaiMeriKahani/tests/image_processing/outputs/bala_pose_one_crop.png")
 
 
 
 
# bala image
filepath = "/home/deepikakhullar/YehHaiMeriKahani/tests/image_processing/outputs/bala_pose_one_crop.png"
img = Image.open(filepath)
img_shape = np.array(img).shape[:-1]
print(img_shape)
bbox_shape = [300, 560]
def resize_to_fit_bbox(img_shape, bbox_shape):
    # Calculate the scaling factors for each dimension
    scale_y = bbox_shape[0] / img_shape[0]
    scale_x = bbox_shape[1] / img_shape[1]

    # Use the smaller scaling factor to maintain the aspect ratio
    scale_factor = min(scale_y, scale_x)

    # Calculate the new dimensions
    new_height = int(img_shape[0] * scale_factor)
    new_width = int(img_shape[1] * scale_factor)

    return (new_height, new_width)
new_img_shape = resize_to_fit_bbox(img_shape, bbox_shape)
print("new img shape", new_img_shape)
resized_img = img.resize((new_img_shape[1], new_img_shape[0]))
# save the resized img
resized_img.save("/home/deepikakhullar/YehHaiMeriKahani/tests/image_processing/outputs/bala_pose_one_crop_resized.png")

# Create a blank canvas with the desired size
canvas = Image.new('RGB', (1280, 960), (0, 0, 0))  # Assuming a black background

# Paste the resized image onto the canvas at the specified coordinates
canvas.paste(resized_img, (650, 500))

canvas.save("/home/deepikakhullar/YehHaiMeriKahani/tests/image_processing/outputs/bala_pose_one_crop_resized_pasted.png")


# dimensions
# {"character":"Simba", "dimensions":[650, 500, 250, 190]}