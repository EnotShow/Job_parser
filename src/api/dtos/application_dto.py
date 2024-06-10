from datetime import datetime
from typing import Optional

from pydantic import AnyUrl

from core.shared.base_dto import BaseDTO
from core.shared.validators import JobResourceURL


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    application_link: AnyUrl
    url: JobResourceURL
    created_at: datetime


class ApplicationFilterDTO(BaseDTO):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[AnyUrl] = None
    url: Optional[JobResourceURL] = None
    owner_id: Optional[int] = None

class ApplicationUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[AnyUrl] = None
    url: Optional[JobResourceURL] = None

class ApplicationUpdateDTO(BaseDTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    application_link: Optional[AnyUrl] = None
    url: Optional[JobResourceURL] = None


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    application_link: AnyUrl
    url: JobResourceURL
    owner_id: int
