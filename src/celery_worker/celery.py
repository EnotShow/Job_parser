from celery import Celery
from core.config.db import settings_broker

celery_app = Celery(
    __name__,
    broker=settings_broker.broker_url,
    backend='redis://',
)

celery_app.autodiscover_tasks(packages=["src.celery_worker.tasks"])

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    autodiscover_tasks=True,
)
