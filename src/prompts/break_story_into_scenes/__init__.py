from ..base import BasePrompt

class BS(BasePrompt):
    def __init__(self):
        super().__init__("break_story_into_scenes")

    
BreakStoryIntoScenesPrompt = BS()