from typing import Optional

from core.shared.base_dto import BaseDTO


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    application_link: str
    url: str


class ApplicationFilterDTO(BaseDTO):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    application_link: Optional[str]
    url: Optional[str]
    owner_id: Optional[int]

class ApplicationUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[str] = None
    url: Optional[str] = None


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    application_link: str
    url: str
    owner_id: int
