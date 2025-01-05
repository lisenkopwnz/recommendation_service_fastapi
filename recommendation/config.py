from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Класс для загрузки и валидации переменных окружения.
    """
    file_system_path:str = Field(default=..., description="FILE_SYSTEM_PATH")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
