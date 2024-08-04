from typing import Union, List, TypeVar

from core.shared.base_dto import BaseDTO
from src.api.middleware.dtos.pagination_dto import PaginationDTO

T = TypeVar('T', bound=BaseDTO)


class BaseService:

    @staticmethod
    def _paginate(dto: Union[List[T], T], page: int, size: int, total: int) -> PaginationDTO:
        return PaginationDTO(page=page, size=size, items=dto, total=total)
