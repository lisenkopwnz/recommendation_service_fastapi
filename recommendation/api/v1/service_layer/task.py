from sqlalchemy.orm import Session

from celery.utils.log import get_task_logger

from recommendation.api.v1.common.unit_of_work import UnionOfWork
from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePandas
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService
from recommendation.config import settings
from recommendation.storage.cache.storage_cache import RedisStorage
from recommendation.storage.cache.storage_manager import CacheStorageManager
from recommendation.storage.db.database_manager import DataBaseService
from recommendation.storage.db.models import SessionLocal
from recommendation.storage.db.sql_alchemy_repository import SQLAlchemyRepository

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def generate_recommendation_task(self):
    db: Session = SessionLocal()  # Создаём сессию
    try:
        # 1. Создаём движок и сервис для рекомендаций
        engine = RecommendationEnginePandas(settings.file_system_path, 20)
        service = RecommendationService(engine)

        # 2. Генерируем рекомендации
        result = service.generate_recommendations()

        # 3. Создаём репозиторий и сервис для работы с БД
        repository = SQLAlchemyRepository(db)
        database_service = DataBaseService(repository)

        # 4. Создаём кеш Redis
        storage = RedisStorage(host='localhost', port=6379, new_db=0, old_db= 1)
        cache_manager = CacheStorageManager(storage)

        # 5. Оборачиваем в UnitOfWork
        with UnionOfWork(database_service, cache_manager) as uow:
            batch_gen = SQLAlchemyRepository.batch_generator(result, batch_size=1000)

            for batch in batch_gen:
                # Обновление базы данных
                database_service.bulk_update(
                    query="""
                        INSERT INTO your_table (id, recommended_ids)
                        VALUES (:id, :recommended_ids)
                        ON CONFLICT (id) DO UPDATE SET
                            recommended_ids = EXCLUDED.recommended_ids;
                    """,
                    params=batch
                )

                # Обновление кеша Redis
                cache_manager.bulk_set(batch)  # Обновление кеша

    except Exception as e:
        logger.error(f"Ошибка в таске generate_recommendation_task: {e}")
        raise self.retry(exc=e)

    finally:
        db.close()  # Закрываем сессию
