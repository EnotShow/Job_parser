from sqladmin import ModelView

from src.models.models import Application


class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.title, Application.url]