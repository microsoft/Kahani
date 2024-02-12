from ..base import BasePrompt


class SummariseCulture(BasePrompt):
    def __init__(self):
        super().__init__("summarise_culture")


SummariseCulturePrompt = SummariseCulture()
