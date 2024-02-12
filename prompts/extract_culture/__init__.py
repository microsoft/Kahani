from ..base import BasePrompt


class ECP(BasePrompt):
    def __init__(self):
        super().__init__("extract_culture")


ExtractCulturePrompt = ECP()
