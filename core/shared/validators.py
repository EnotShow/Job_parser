from typing import Annotated

from core.shared.errors import ResourceError
from src.parsers import base_urls


class JobResourceURL(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        for i in base_urls:
            if value.startswith(i):
                return cls(value)
        raise ResourceError('invalid resource url')

    def __repr__(self):
        return f'JobResourceURL({super().__repr__()})'