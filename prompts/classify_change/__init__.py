from llm import fn
from ..base import BasePrompt


class CC(BasePrompt):
    def __init__(self):
        super().__init__("classify_change")

    def __call__(self, **kwargs):
        kwargs['tools'] = [
            fn('update_story', 'Update the current story', {'change': {
                'type': 'string', 'description': 'instructions from the user'}}, ['change']),
            fn('update_character', 'Update a character in the story across all scenes. This change is not scene specific', {'name': {
                'type': 'string', 'description': 'name of the character'}, 'change': {
                'type': 'string', 'description': 'instructions from the user'}}, ['name', 'change']),
            fn('update_scene', 'Update a specific scene in the story. It could include changes to the action of the character.', {'scene_number': {
                'type': 'integer', 'description': '0-index scene number'},
                'change': {
                    'type': 'string', 'description': 'instructions from the user'}}, ['change', 'scene_number']),
        ]
        super().__call__(**kwargs)


ClassifyChangePrompt = CC()
