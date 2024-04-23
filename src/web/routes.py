from fastapi import FastAPI
import flet as ft
import flet.fastapi as flet_fastapi

from src.web.views.login import login_view
from src.web.views.main import main


def add_web_routes(app: FastAPI):
    app.mount("/login", flet_fastapi.app(login_view))
    app.mount("/", flet_fastapi.app(main))
