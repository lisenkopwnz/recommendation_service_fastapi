from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    """
    Класс для загрузки и валидации переменных окружения.
    """
    path_uploaded_data_file:str = Field(default=str(BASE_DIR), description="The path to the uploaded data file")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
