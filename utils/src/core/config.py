import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings
from pydantic import Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RedisSettings(BaseSettings):
    host: str = Field(env='REDIS_HOST', default='127.0.0.1')
    port: int = Field(env='REDIS_PORT', default='6379')

    class Config:
        env_file = '../../../config/.env.app'


class ESSettings(BaseSettings):
    es_host: str = Field(env='ELASTIC_HOST', default='127.0.0.1')
    es_port: int = Field(env='ELASTIC_PORT', default='9200')

    class Config:
        env_file = '../../../config/.env.app'


class StateSettings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(env='PROJECT_NAME')

    class Config:
        env_file = '../../../config/.env.app'
