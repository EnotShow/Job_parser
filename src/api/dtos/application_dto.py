from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

from pydantic import AnyUrl, AfterValidator
from pydantic_core import Url

from core.shared.base_dto import BaseDTO
from core.shared.validators import JobResourceURL

AnyUrl = Annotated[AnyUrl, AfterValidator(str)]


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    application_link: AnyUrl
    url: AnyUrl  # JobResourceURL
    short_id: Optional[UUID] = None
    applied: Optional[bool] = None
    application_date: Optional[datetime] = None
    created_at: datetime

    @property
    def short_url(self) -> Url:
        return f"{self.settings.base_url}/applications/{self.short_id}"


class ApplicationFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[AnyUrl] = None
    url: Optional[AnyUrl] = None
    owner_id: Optional[int] = None


class ApplicationUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[AnyUrl] = None
    url: Optional[AnyUrl] = None
    short_id: Optional[UUID] = None
    applied: Optional[bool] = None
    application_date: Optional[datetime] = None


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    application_link: AnyUrl
    url: AnyUrl
    owner_id: int

    @property
    def short_url(self) -> Url:
        return f"{self.settings.base_url}/applications/{self.short_id}"