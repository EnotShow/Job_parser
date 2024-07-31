from typing import List, TypeVar, Generic

from core.shared.base_dto import BaseDTO

T = TypeVar('T', bound=BaseDTO)


class PaginationDTO(BaseDTO, Generic[T]):
    page: int
    size: int
    items: List[T]


class PaginationParams(BaseDTO):
    page: int
    size: int
