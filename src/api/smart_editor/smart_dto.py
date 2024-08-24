from typing import List

from core.shared.base_dto import BaseDTO
from src.parsers.enums import ServiceEnum


class SmartEditorParamsDTO(BaseDTO):
    kwords: str
    location: str
    salary: str
    services: List[ServiceEnum]
    owner_id: int
    links_limit: List[str]
