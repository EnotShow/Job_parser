from sqladmin import ModelView

from src.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.email]
