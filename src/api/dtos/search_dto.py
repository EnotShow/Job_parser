from typing import Optional

from core.shared.base_dto import BaseDTO


class SearchDTO(BaseDTO):
    id: int
    title: str
    url: str
    owner_id: int


class SearchFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    owner_id: Optional[int] = None


class SearchUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    url: Optional[str] = None


class SearchCreateDTO(BaseDTO):
    title: str
    url: str
    owner_id: int
