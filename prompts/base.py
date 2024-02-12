import os
from llm import sm, um, llm

class BasePrompt(object):
    _cache = {}

    @classmethod
    def read_local(cls, name, subdir="", extension=".md"):
        cache_key = f"{subdir}_{name}"
        if cache_key not in cls._cache:
            file_path = os.path.join(os.path.dirname(
                __file__), subdir, name + extension)
            with open(file_path) as f:
                cls._cache[cache_key] = f.read()
        return cls._cache[cache_key]

    def __init__(self, subdir):
        self.subdir = subdir

    def create_prompt(self, **kwargs):
        system_prompt = self.read_local("system", self.subdir)
        user_prompt = self.read_local("user", self.subdir)

        return [
            sm(system_prompt.format(**kwargs)),
            um(user_prompt.format(**kwargs)),
        ]

    def __call__(self, **kwargs):
        if 'messages' not in kwargs:
            messages = self.create_prompt(**kwargs)
            kwargs['messages'] = messages
        return llm(**kwargs)
