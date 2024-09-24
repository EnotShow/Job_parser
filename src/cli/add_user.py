import click
from dependency_injector.wiring import inject, Provide

from core.shared.errors import AlreadyExistError
from src.api.auth.auth_dto import UserRegisterDTO
from src.api.auth.containers.auth_service_container import AuthServiceContainer
from src.api.auth.services.auth_service import AuthService
from src.cli.helpers import run_command_async
from src.containers_builder import build_containers


@inject
async def add_user(auth_service: AuthService = Provide[AuthServiceContainer.auth_service]):
    # User input
    email = click.prompt('Please enter your email', type=str)
    # Password checking
    while True:
        password = click.prompt('Please enter your password', type=str, hide_input=True)
        password2 = click.prompt('Please repeat your password', type=str, hide_input=True)
        if password == password2:
            break
        print("Passwords don't match. Try again.")

    # User creation
    user = UserRegisterDTO(
        email=email,
        password=password,
        language_code="en"
    )
    try:
        await auth_service.register(user)
        print("User created successfully!")
        return
    except AlreadyExistError:
        print("User already exists!")
        exit(1)
    except Exception as e:
        print("Unexpected error: " + str(e))
        exit(1)


@click.command(name="create-admin")
def add_user_async():
    """Create admin user"""
    build_containers()

    run_command_async(add_user())
