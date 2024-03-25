from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    email: str


class UserCreateDTO(BaseDTO):
    email: str
    password: str
