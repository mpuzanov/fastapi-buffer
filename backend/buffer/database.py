from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import json
from .config import settings, logger


engine = create_engine(settings.database_url, fast_executemany=True, echo=False)


Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class DbRedis:
    def __init__(self):
        self.conn = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    def is_redis_available(self):
        try:
            self.conn.ping()
        except (redis.exceptions.ConnectionError, ConnectionRefusedError) as ex:
            logger.error(f"{__class__.__name__} {ex}")
            return False
        return True

    def get(self, key):
        if self.is_redis_available():
            try:
                data = self.conn.get(key)
                if data:
                    logger.debug(f'взяли из redis: {key}')
                    return json.loads(data)
            except Exception as ex:
                logger.error(f"{__class__.__name__} {ex}")
            else:
                return None
        else:
            return None

    def set(self, key, value, time_ex: int = 3600):
        if self.is_redis_available():
            try:
                self.conn.set(key, json.dumps(value), ex=time_ex)
                logger.debug(f'сохранили в redis: {key}')
            except Exception as ex:
                logger.error(f"{__class__.__name__} {ex}")
