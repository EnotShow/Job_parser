from core.shared.base_dto import BaseDTO


class SearchDTO(BaseDTO):
    id: int
    title: str
    url: str


class SearchCreateDTO(BaseDTO):
    title: str
    url: str
    owner: int
