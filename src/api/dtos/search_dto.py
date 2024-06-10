from typing import Optional

from core.shared.base_dto import BaseDTO
from core.shared.validators import JobResourceURL


class SearchDTO(BaseDTO):
    id: int
    title: str
    url: JobResourceURL
    owner_id: int


class SearchFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[JobResourceURL] = None
    owner_id: Optional[int] = None


class SearchUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    url: Optional[JobResourceURL] = None


class SearchCreateDTO(BaseDTO):
    title: str
    url: JobResourceURL
    owner_id: int
