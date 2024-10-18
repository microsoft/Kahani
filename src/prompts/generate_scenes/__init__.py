from ..base import BasePrompt

class GS(BasePrompt):
    def __init__(self):
        super().__init__("generate_scenes")

GenerateScenesPrompt = GS()