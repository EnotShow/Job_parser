from fastapi import BackgroundTasks

from src.config.email.email_config import config_email
from src.lib.email.client import EmailClient
from src.lib.email.consts import EmailSubject, TemplatesPath
from src.lib.email.email_dto import EmailDTO


class EmailService:
    """Сервис для работы с отправкой email"""

    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.tasks = background_tasks
        self.email_client = EmailClient()

    async def send_register_email(self, user_email: str, code: str) -> None:
        dto = EmailDTO(
            template_path=TemplatesPath.ACTIVATION.value,
            email_subject=EmailSubject.ACTIVATION.value,
            recipient=user_email,
            context={"email": user_email, "code": code},
        )
        self.tasks.add_task(self.email_client.send_email, dto)

    async def send_admin_email(self, mentor_email: str) -> None:
        dto = EmailDTO(
            template_path=TemplatesPath.ADMIN_ALERT.value,
            email_subject=EmailSubject.ADMIN_ALERT.value,
            recipient=config_email.ADMINS,
            context={"email": mentor_email},
        )
        self.tasks.add_task(self.email_client.send_email, dto)

    async def send_password_recovery_email(self, user_email: str, code: str) -> None:
        dto = EmailDTO(
            template_path=TemplatesPath.PASSWORD_RECOVERY.value,
            email_subject=EmailSubject.PASSWORD_RECOVERY.value,
            recipient=user_email,
            context={"email": user_email, "code": code},
        )
        self.tasks.add_task(self.email_client.send_email, dto)
