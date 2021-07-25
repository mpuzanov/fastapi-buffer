import os
from pydantic import BaseSettings
import backend.buffer.internal.app_logger as log
from icecream import ic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_XML = '<?xml version="1.0" encoding="UTF-8"?>'


class Settings(BaseSettings):

    class Config:
        env_file = os.path.join(BASE_DIR, '.env')

    debug: bool = bool(os.environ.get('DEBUG', False))
    newrelic_config: str = os.path.join(BASE_DIR, 'newrelic.ini')
    base_dir: str = BASE_DIR
    autoreload: bool = True
    root_path: str = ''
    service_host: str = '0.0.0.0'
    service_port: int = 13050
    logs_file: str = 'buffer.log'
    database_url: str = ''
    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600
    log_level: str = 'DEBUG' if debug else 'INFO'


settings = Settings()
settings.log_level = 'DEBUG' if settings.debug else 'INFO'

logger = log.get_logger(__name__, settings.log_level, settings.logs_file)
logger.debug(f'BASE_DIR: {BASE_DIR}')
logger.debug(f'database_url: {settings.database_url}')
logger.debug(f'log_level: {settings.log_level}')
ic(BASE_DIR)
ic(settings.log_level)
ic(settings.database_url)
