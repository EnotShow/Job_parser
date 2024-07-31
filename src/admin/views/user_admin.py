from sqladmin import ModelView

from src.api.users.user_model import User


class UserAdmin(ModelView, model=User):
    column_list = [User.email]
