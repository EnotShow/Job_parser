from celery.exceptions import TaskError

from core.shared.email.client import EmailClient
from src.api.email.email_dto import EmailDTO
from src.celery_worker.celery import celery_app




@celery_app.task(bind=True, autoretry_for=(TaskError,), retry_kwargs={"max_retries": 2})
def send_email(self, dto: dict):
    dto = EmailDTO(**dto)
    client = EmailClient()
    client.send_email(dto)
