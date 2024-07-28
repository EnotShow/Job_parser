import asyncio
from typing import Generic, TypeVar, Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from core.shared.base_dto import BaseDTO
from src.api.dtos.pagination_dto import PaginationDTO

T = TypeVar('T', bound=BaseDTO)


class BaseRepository:

    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    def __del__(self):
        if self._session is not None:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
            loop.create_task(self._session.close())

    @staticmethod
    def _paginate(dto: Union[List[T], T], page: int, size: int):
        return PaginationDTO(page=page, size=size, items=dto)
