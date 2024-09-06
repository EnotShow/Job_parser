from pydantic import FilePath, EmailStr

from core.shared.base_dto import BaseDTO


class EmailDTO(BaseDTO):
    template: FilePath
    email_subject: str
    recipient: EmailStr
    context: dict[str, str]
