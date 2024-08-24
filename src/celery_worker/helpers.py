from typing import List, TypeVar

from core.shared.base_dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)


def convert_to_celery_primitive(objects: List[T]) -> List[T]:
    return [obj.model_dump() for obj in objects]
