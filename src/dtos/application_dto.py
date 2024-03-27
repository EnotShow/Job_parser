from core.shared.base_dto import BaseDTO


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    description: str
    application_link: str
    url: str


class ApplicationCreateDTO(BaseDTO):
    title: str
    description: str
    application_link: str
    url: str
