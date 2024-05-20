from core.shared.base_dto import BaseDTO


class UserDTO(BaseDTO):
    id: int
    email: str
    language_code: str


class UserCreateDTO(BaseDTO):
    email: str
    language_code: str
