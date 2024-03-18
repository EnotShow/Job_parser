from core.shared.base_dto import BaseDTO


class ApplicationDTO(BaseDTO):
    id: int
    title: str
    url: str


class ApplicationCreateDTO(BaseDTO):
    title: str
    url: str
