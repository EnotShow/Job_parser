import flet as ft


async def login_view(page: ft.Page):

    def authenticate(e):
        print(username.value, password.value)
        page.go("/some")

    page.title = "Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", width=300, password=True)
    login = ft.ElevatedButton("Login", width=300)

    page.add(username, password, login)

    login.on_click = authenticate
