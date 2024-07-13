from datetime import datetime
from typing import Optional, Annotated

from pydantic import AnyUrl, AfterValidator

from core.shared.base_dto import BaseDTO
from core.shared.validators import JobResourceURL

AnyUrl = Annotated[AnyUrl, AfterValidator(str)]


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    application_link: AnyUrl
    url: AnyUrl # JobResourceURL
    created_at: datetime


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


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    application_link: AnyUrl
    url: AnyUrl
    owner_id: int
