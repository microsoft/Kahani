from ..base import BasePrompt

class GeneratePose(BasePrompt):
    def __init__(self):
        super().__init__("generate_pose")
        
GeneratePosePrompt = GeneratePose()
    
