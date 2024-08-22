# Job Parser

#### Before running project make sure you have a correct .env file. An example can be found on .env.dev file.

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
   python -m flower --broker=redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0 flower
   ```

### Celery
   ```
   celery -A src.celery_worker worker --loglevel=INFO
   ```


## Backend 
1) Install poetry
   ```
   pip install poetry
   ```
2) Next install poetry dependency
   ```
   poetry install
   ```
3) Run application
   ```
   python app.py
   ```

## Front
1) Go to a front folder
   ```
   cd front
   ```
2) Install React dependency
   ```
   npm install
   ```
3) Run front-end
   ```
   npm run
   ```
   
#### You can run databases from docker and other services locally in this case make sure that in those case you need to configure right parameters for each run

##### .env params for docker run
```
POSTGRES_HOST=postgres
REDIS_HOST=redis
```

##### .env params for local run
```
POSTGRES_HOST={TARGET__POSTGRES_HOST}
REDIS_HOST={TARGET_REDIS_HOST}
```
#### Example
```
POSTGRES_HOST=127.0.0.1
REDIS_HOST=127.0.0.1
```

   
## Docker compose

<b>docker-compose.yml</b> - Main docker compose file. Include all the services runned on a main server: postgres, redis, flower, backend, frontend

<b>docker-compose-local.yml</b> - Docker compose for local development. Include all the services from a main docker + worker

<b>docker-compose-mq.yml</b> - Docker compose for testing MQ and worker. Include redis, flower and worker service

<b>docker-compose-traefik.yml</b> - Docker compose file for deploying in production using traefik

To run docker compose file use:
```
docker compose -f {DOCKER FILE} up --build -d
```
