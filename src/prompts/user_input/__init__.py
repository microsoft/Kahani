from ..base import BasePrompt

class UI(BasePrompt):
    def __init__(self):
        super().__init__("user_input")
    
UserInputPrompt = UI()