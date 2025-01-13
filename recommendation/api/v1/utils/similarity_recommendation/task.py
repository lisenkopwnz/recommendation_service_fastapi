from sqlalchemy.orm import Session

from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePandas
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService
from recommendation.config import settings
from recommendation.db.database_service import DataBaseService
from recommendation.db.models import SessionLocal
from recommendation.db.sql_alchemy_repository import SQLAlchemyRepository


@shared_task
def generate_recommendation_task():
    db: Session = SessionLocal()
    try:
        # Создаём движок
        engine = RecommendationEnginePandas(settings.file_system_path, 20)

        # Создаём сервис и передаём ему движок
        service = RecommendationService(engine)

        # Генерируем рекомендации
        result = service.generate_recommendations()

        # Создаём репозиторий и сервис для работы с базой данных
        repository = SQLAlchemyRepository(db)
        database_service = DataBaseService(repository)

        # Преобразуем результат в генератор пакетов
        batch_gen = SQLAlchemyRepository.batch_generator(result, batch_size=1000)

        # Выполняем массовое обновление
        database_service.bulk_update(
            query="""
                INSERT INTO your_table (id, recommended_ids)
                VALUES (:id, :recommended_ids)
                ON CONFLICT (id) DO UPDATE SET
                    recommended_ids = EXCLUDED.recommended_ids;
            """,
            params=batch_gen
        )
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем сессию
        db.close()
