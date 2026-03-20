from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = Field(default='宠物课堂')
    api_v1_prefix: str = Field(default='/api/v1')
    debug: bool = Field(default=True)

    mysql_host: str = Field(default='127.0.0.1')
    mysql_port: int = Field(default=3306)
    mysql_user: str = Field(default='root')
    mysql_password: str = Field(default='123456')
    mysql_db: str = Field(default='class_pets')
    database_url: str | None = Field(default=None)

    points_per_level: int = Field(default=100)
    allow_negative_points: bool = Field(default=False)

    @field_validator('debug', mode='before')
    @classmethod
    def normalize_debug(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return True
        text = str(value).strip().lower()
        if text in {'1', 'true', 'yes', 'on', 'debug'}:
            return True
        if text in {'0', 'false', 'no', 'off', 'release', 'prod', 'production'}:
            return False
        return True

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f'mysql+pymysql://{self.mysql_user}:{self.mysql_password}'
            f'@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4'
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
