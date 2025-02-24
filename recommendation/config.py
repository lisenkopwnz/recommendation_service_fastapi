from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    """
    Класс для загрузки и валидации переменных окружения.
    """
    path_uploaded_data_file: str = Field(default=str(BASE_DIR),
                                         description="The directory path where uploaded data files are stored.")
    redis_host: str = Field(default='redis', description="Host address for the Redis server.")
    redis_port: int = Field(default=6379, description="Port number for connecting to the Redis server.")
    new_db: int = Field(default=0, description="The Redis database index to use for new data.")
    old_db: int = Field(default=1, description="The Redis database index to use for old data.")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
