from datetime import datetime
from typing import Optional, Annotated

from pydantic import AnyUrl, AfterValidator

from core.shared.base_dto import BaseDTO
from core.shared.validators import JobResourceURL

AnyUrl = Annotated[AnyUrl, AfterValidator(str)]


class SearchDTO(BaseDTO):
    id: int
    title: str
    url: JobResourceURL
    created_at: datetime
    owner_id: int


class SearchFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[AnyUrl] = None
    owner_id: Optional[int] = None


class SearchUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    url: Optional[AnyUrl] = None


class SearchCreateDTO(BaseDTO):
    title: str
    url: AnyUrl
    owner_id: int
