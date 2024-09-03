from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

from pydantic import AnyUrl, AfterValidator
from pydantic_core import Url

from core.config.proj_settings import settings
from core.shared.base_dto import BaseDTO
from src.api.users.user_dto import UserDTO

AnyUrl = Annotated[AnyUrl, AfterValidator(str)]


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    url: str  # JobResourceURL
    short_id: Optional[UUID] = None
    applied: Optional[bool] = None
    application_date: Optional[datetime] = None
    created_at: datetime
    owner_id: int

    @property
    def short_url(self) -> Url:
        return f"{settings.base_url}/applications/apply/{self.short_id}"


class ApplicationFullDTO(BaseDTO):
    id: int
    title: str
    description: str
    url: str
    short_id: Optional[UUID] = None
    applied: Optional[bool] = None
    application_date: Optional[datetime] = None
    created_at: datetime
    owner_id: int
    owner: UserDTO

    @property
    def short_url(self) -> Url:
        return f"{settings.base_url}/applications/apply/{self.short_id}"


class ApplicationFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[AnyUrl] = None
    owner_id: Optional[int] = None
    short_id: Optional[UUID] = None


class ApplicationUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[AnyUrl] = None
    short_id: Optional[UUID] = None
    applied: Optional[bool] = None
    application_date: Optional[datetime] = None


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    url: AnyUrl
    owner_id: int
