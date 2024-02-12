from pydantic import BaseModel


class Scene(BaseModel):

    narration: str
    backdrop: str
    prompt: str = None
    image: str = None
    characters: dict[str, str] = {}    


class Character(BaseModel):

    name: str
    description: str
    prompt: str = None
    scene_prompt: str = None
    image: str = None
    image_pose: str = None
    scenes: list[int] = []    


class Story(BaseModel):

    story: str = None
    cultural_context: str = None
    scenes: list[Scene] = []
    characters: list[Character] = []
