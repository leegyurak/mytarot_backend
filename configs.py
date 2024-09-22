import os
from typing import Any

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_host: str = os.environ.get('MYSQL_HOST')
    db_port: str = os.environ.get('MYSQL_PORT')
    db_name: str = os.environ.get('MYSQL_DATABASE')
    db_user: str = os.environ.get('MYSQL_USER')
    db_password: str = os.environ.get('MYSQL_PASSWORD')

    class Config:
        extra = 'allow'

    @property
    def url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    

class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

    env: str = os.environ.get('ENV')
    claude_api_key: str = os.environ.get('CLAUDE_API_KEY')
    API_PREFIX: str = "/api/v1/"

    class Config:
        extra = 'allow'
        
    def model_dump(self):
        model_dumped_dict: dict[str, Any] = super().model_dump()
        model_dumped_dict['db']['url'] = self.db.url
        return model_dumped_dict


settings: ApplicationSettings = ApplicationSettings()
