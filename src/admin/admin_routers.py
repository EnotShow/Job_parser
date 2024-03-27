from sqladmin import Admin

from src.admin.views.application_admin import ApplicationAdmin
from src.admin.views.searches_admin import SearchAdmin
from src.admin.views.user_admin import UserAdmin


def add_admin_views(admin: Admin):
    admin.add_view(ApplicationAdmin)
    admin.add_view(SearchAdmin)
    admin.add_view(UserAdmin)
