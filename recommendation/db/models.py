from sqlalchemy import create_engine, Column, Integer, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base

# Получаем переменные окружения
import os
POSTGRES_USER = os.getenv("POSTGRES_USER", "myuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "mydatabase")

# Формируем строку подключения
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SimilarContentRecommendation(Base):
    __tablename__ = "similar_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(ARRAY(Integer))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())  # Время создания
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()) # Время обновления

Base.metadata.create_all(bind=engine)