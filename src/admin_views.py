from sqladmin import Admin

from src.admin.application_admin import ApplicationAdmin
from src.admin.searches_admin import SearchAdmin


def add_admin_views(admin: Admin):
    admin.add_view(ApplicationAdmin)
    admin.add_view(SearchAdmin)