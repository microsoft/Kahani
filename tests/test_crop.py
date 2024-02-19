import cv2
import numpy as np
from unittest import TestCase


class TestCrop(TestCase):

    def test_basic(self):

        # Load your image (replace 'your_image.png' with your image file)
        image = cv2.imread('output.png')

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find contours
        contours, _ = cv2.findContours(
            gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        print(x, y, w, h)

        # Crop the image
        cropped_image = image[y:y+h, x:x+w]

        # Save or display the cropped image
        cv2.imwrite('output_cropped.png', cropped_image)
        # cv2.imshow('Cropped Image', cropped_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
