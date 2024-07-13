# Job Parser

## How to make migrations?
1) Import module with models to `migrations/base.py`.

2) Execute a command to make migration file
    ```
    alembic revision --autogenerate -m 'Model name or migration title'
    ```
3) Check the created migration file. WARNING!!! Alembic can't do model renaming automatically.

4) Make migration (make changes in db)
    ```
    alembic upgrade head
    ```

## Celery workers

### Flower
   ```
   python -m flower --broker=amqp://rabbitmq:rabbitmq@localhost:5672/ flower
   ```

### Celery
   ```
   celery -A src.celery_worker worker --loglevel=INFO
   ```