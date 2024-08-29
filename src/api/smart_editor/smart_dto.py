from typing import List, Optional

from core.shared.base_dto import BaseDTO
from src.parsers.enums import ServiceEnum


class SmartEditorParamsDTO(BaseDTO):
    kwords: str
    location: str
    salary: str
    services: List[ServiceEnum]
    owner_id: int
    links_limit: int


class SmartProcessHashDTO(BaseDTO):
    pk: Optional[str] = None
    user_id: Optional[int]
