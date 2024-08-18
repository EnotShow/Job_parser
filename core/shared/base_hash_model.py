from aredis_om import HashModel, get_redis_connection

from core.config.db import settings_broker


class BaseHashModel(HashModel):
    class Meta:
        global_key_prefix = __qualname__
        database = get_redis_connection(url=settings_broker.broker_url, decode_responses=True)
