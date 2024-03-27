from sqladmin import ModelView

from src.models.search import Search


class SearchAdmin(ModelView, model=Search):
    column_list = [Search.title, Search.url]
