from ..base import BasePrompt


class B(BasePrompt):

    def __init__(self):
        super().__init__("bounding_box")


BoundingBoxPrompt = B()
