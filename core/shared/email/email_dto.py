from core.shared.base_dto import BaseDTO


class EmailDTO(BaseDTO):
    template_path: str
    email_subject: str
    recipient: str
    context: dict[str, str]
