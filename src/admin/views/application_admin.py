from sqladmin import ModelView

from src.api.applications.application_model import Application


class ApplicationAdmin(ModelView, model=Application):
    column_list = [Application.title, Application.url]
    save_as = True
