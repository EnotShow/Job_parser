from sqladmin import ModelView

from src.api.models import Application


class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.title, Application.url]
    save_as = True
