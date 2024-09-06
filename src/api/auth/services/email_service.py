from core.shared.email.consts import EmailSubject, EmailTemplate
from src.api.email.email_dto import EmailDTO
from src.api.email.service import BaseEmailService


class EmailService:
    """Сервис для работы с отправкой email, связанных с аутентификацией пользователя."""

    def __init__(self) -> None:
        self._base_email_service = BaseEmailService()

    async def send_register_email(self, user_email: str, code: str) -> None:
        """Gather EmailDTO and run base method."""
        dto = EmailDTO(
            template=EmailTemplate.ACTIVATION.value,
            email_subject=EmailSubject.ACTIVATION.value,
            recipient=user_email,
            context={"email": user_email, "code": "code"},
        )
        await self._base_email_service.send_email(dto)
