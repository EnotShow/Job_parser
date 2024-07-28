from src.api.dtos.pagination_dto import PaginationDTO


class BaseService:

    @staticmethod
    def _unpack_items(pagination_dto: PaginationDTO):
        if len(pagination_dto.items) == 1:
            return pagination_dto.items[0]
        return pagination_dto.items
