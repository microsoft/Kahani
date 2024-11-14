from ..base import BasePrompt

class CS(BasePrompt):
    def __init__(self):
        super().__init__("create_story")
    
CreateStoryPrompt = CS()