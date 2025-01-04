from sqlalchemy import create_engine, Column, Integer, ARRAY, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"

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