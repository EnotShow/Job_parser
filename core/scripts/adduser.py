import getpass

from core.db.db_helper import db_helper
from src.auth.service import auth_service
from src.dtos.user_dto import UserCreateDTO
from src.repositories.user_repository import UserRepository


async def add_user():
    email = input("Enter user email: ")
    while True:
        password = getpass.getpass("Enter user password: ")
        password2 = getpass.getpass("Enter user password again: ")
        if password == password2:
            async with db_helper.get_db_session() as session:
                encoded_password = await auth_service.encode_password(password)
                user = UserCreateDTO(email=email, password=encoded_password)
                await UserRepository(session).create(user)
                print("User created successfully!")
                exit(1)
        else:
            print("Passwords don't match. Try again.")