from .extract_culture import ExtractCulturePrompt
from .create_story import CreateStoryPrompt
from .extract_characters import ExtractCharactersPrompt
from .break_story_into_scenes import BreakStoryIntoScenesPrompt
from .classify_change import ClassifyChangePrompt
from .summarise_culture import SummariseCulturePrompt
from .generate_scenes import GenerateScenesPrompt
from .generate_character import GenerateCharactersPrompt
from .bounding_box import BoundingBoxPrompt
from .generate_pose import GeneratePosePrompt
from .user_input import UserInputPrompt


__all__ = [
    "ExtractCulturePrompt",
    "CreateStoryPrompt",
    "ExtractCharactersPrompt",
    "BreakStoryIntoScenesPrompt",
    "ClassifyChangePrompt",
    "SummariseCulturePrompt",
    "GenerateScenesPrompt",
    "GenerateCharactersPrompt",
    "BoundingBoxPrompt",
    "GeneratePosePrompt",
    "UserInputPrompt",
]
