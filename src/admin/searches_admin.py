from sqladmin import ModelView

from src.models.models import Search


class SearchAdmin(ModelView, model=Search):
    column_list = [Search.title, Search.url]
