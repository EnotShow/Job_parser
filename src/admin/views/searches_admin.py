from sqladmin import ModelView

from src.api.searches.search_model import Search


class SearchAdmin(ModelView, model=Search):
    column_list = [Search.title, Search.url]
