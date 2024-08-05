from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

from pydantic import AnyUrl, AfterValidator

from core.shared.base_dto import BaseDTO

AnyUrl = Annotated[AnyUrl, AfterValidator(str)]


class SearchDTO(BaseDTO):
    id: UUID
    title: str
    url: AnyUrl
    created_at: datetime
    owner_id: int


class SearchFilterDTO(BaseDTO):
    id: Optional[UUID] = None
    title: Optional[str] = None
    url: Optional[AnyUrl] = None
    owner_id: Optional[int] = None


class SearchUpdateDTO(BaseDTO):
    id: UUID
    title: Optional[str] = None
    url: Optional[AnyUrl] = None


class SearchCreateDTO(BaseDTO):
    title: str
    url: AnyUrl
    owner_id: int
