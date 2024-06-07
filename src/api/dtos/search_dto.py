from typing import Optional

from core.shared.base_dto import BaseDTO


class SearchDTO(BaseDTO):
    id: int
    title: str
    url: str


class SearchFilterDTO(BaseDTO):
    id: Optional[int]
    title: Optional[str]
    url: Optional[str]
    owner: Optional[str]


class SearchCreateDTO(BaseDTO):
    title: str
    url: str
    owner: int
