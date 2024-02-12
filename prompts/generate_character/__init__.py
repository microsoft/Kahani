from ..base import BasePrompt

class GenerateCharacters(BasePrompt):
    def __init__(self):
        super().__init__("generate_character")
    
GenerateCharactersPrompt = GenerateCharacters()