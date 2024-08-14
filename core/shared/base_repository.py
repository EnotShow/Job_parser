from aredis_om import get_redis_connection


class BaseRepository:
    pass


class CacheRepository:
    model = None

    def __init__(self):
        if self.model is None:
            raise NotImplementedError('Repository "model" parameter is not defined')

