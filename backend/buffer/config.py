import os
from pydantic import BaseSettings
import backend.buffer.internal.app_logger as log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_XML = '<?xml version="1.0" encoding="UTF-8"?>'

class Settings(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, '.env')

    debug = bool(os.environ.get('Debug', False))
    newrelic_config: str = os.path.join(BASE_DIR, 'newrelic.ini')
    base_dir: str = BASE_DIR
    autoreload = True
    root_path = ''
    service_host = 'localhost'
    service_port: int = 13050
    log_level = 'DEBUG' if debug else 'INFO'
    logs_file: str = 'buffer.log'
    database_url: str = ''


settings = Settings()

logger = log.get_logger(__name__, settings.log_level, settings.logs_file)

logger.debug(f'BASE_DIR: {BASE_DIR}')
logger.debug(f'database_url: {settings.database_url}')
logger.debug(f'log_level: {settings.log_level}')
