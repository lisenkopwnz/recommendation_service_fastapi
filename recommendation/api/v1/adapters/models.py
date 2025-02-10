from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ARRAY, TIMESTAMP, func
import os

# Подключение к базе данных через асинхронный драйвер
POSTGRES_USER = os.getenv("POSTGRES_USER", "myuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "storage")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "mydatabase")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создание асинхронного движка
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()

class SimilarContentRecommendation(Base):
    __tablename__ = "similar_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(ARRAY(Integer))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())  # Время создания
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())  # Время обновления

# Асинхронное создание таблиц
async def init_db():
    async with engine.begin() as conn:
        # Создаем таблицы через асинхронный коннектор
        await conn.run_sync(Base.metadata.create_all)

