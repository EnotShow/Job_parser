from sqladmin import ModelView

from src.models.application import Application


class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.title, Application.url]