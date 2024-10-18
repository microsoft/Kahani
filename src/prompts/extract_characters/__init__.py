from ..base import BasePrompt

class ExtractCharacters(BasePrompt):
    def __init__(self):
        super().__init__("extract_characters")
    
ExtractCharactersPrompt = ExtractCharacters()