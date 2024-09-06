from celery.exceptions import TaskError

from src.api.email.email_dto import EmailDTO
from src.celery_worker.email_worker.tasks import send_email


class BaseEmailService:

    @staticmethod
    async def send_email(dto: EmailDTO) -> None:
        """Set a task to Celery."""
        try:
            send_email.apply_async((dto.model_dump(),))
        except TaskError:
            pass
