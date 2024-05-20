from sqladmin import ModelView

from src.api.models import Search


class SearchAdmin(ModelView, model=Search):
    column_list = [Search.title, Search.url]
