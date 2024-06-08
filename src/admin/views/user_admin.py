from sqladmin import ModelView

from src.api.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.email]
