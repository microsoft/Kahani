import cv2
import numpy as np
from unittest import TestCase


class TestCrop(TestCase):

    def test_basic(self):

        # Load your image (replace 'your_image.png' with your image file)
        image = cv2.imread('output_cropped.png')

        # Ensure the image has an alpha channel, if not add one
        if image.shape[2] == 3:  # No alpha channel
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find contours
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Create an all zero mask with the same dimensions as the image
        mask = np.zeros_like(gray)

        # Draw the largest contour on the mask with white color and filled
        cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, 255, thickness=cv2.FILLED)

        # Create an alpha channel based on the inverse of the mask
        alpha_channel = np.ones_like(gray, dtype=np.uint8) * 255  # full opacity
        alpha_channel[mask == 255] = 0  # set transparency where mask is filled

        # Combine the original image with the new alpha channel
        result = cv2.merge([image[:, :, 0], image[:, :, 1], image[:, :, 2], alpha_channel])

        # Save or display the result
        cv2.imwrite('transparent_image.png', result)
        # cv2.imshow('Transparent Image', result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()