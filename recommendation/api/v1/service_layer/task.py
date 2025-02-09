from sqlalchemy.orm import Session
from celery.utils.log import get_task_logger
from recommendation.api.v1.common.unit_of_work import UnionOfWork
from recommendation.api.v1.service_layer.managers import create_database_manager, create_cache_manager
from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePandas
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService
from recommendation.config import settings
from recommendation.api.v1.adapters.models import SessionLocal
from recommendation.api.v1.adapters.database_sql_alchemy import SQLAlchemyRepository

# Логгер для Celery
logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def generate_recommendation_task(self):
    """
    Главная задача для генерации рекомендаций и обновления базы данных и кеша Redis.

    Эта задача выполняет следующие шаги:
    1. Инициализирует движок и сервис для генерации рекомендаций.
    2. Генерирует рекомендации для видео.
    3. Создаёт репозиторий и сервис для работы с базой данных.
    4. Создаёт кеш Redis.
    5. Обновляет базу данных и кеш Redis с помощью UnitOfWork.
    """
    # Создаем сессию для работы с базой данных
    db: Session = SessionLocal()

    try:
        # 1. Создаём движок и сервис для рекомендаций
        engine = RecommendationEnginePandas(settings.file_system_path, 20)
        service = RecommendationService(engine)

        # 2. Генерируем рекомендации
        result = service.generate_recommendations()

        # 3. Создаём сервис и низкоуровневую реализацию для работы с БД
        database_service = create_database_manager(db)

        # 4. Создаём сервис и низкоуровневую реализацию для работы с кешем
        cache_manager = create_cache_manager(host='localhost', port=6379, new_db=0, old_db=1)

        # 5. Оборачиваем в UnitOfWork для атомарных операций
        with UnionOfWork(database_service, cache_manager) as uow:
            # Генерация пакетов данных для массового обновления
            batch_gen = SQLAlchemyRepository.batch_generator(result, batch_size=1000)

            for batch in batch_gen:
                # Обновление базы данных с использованием bulk update
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
                cache_manager.bulk_set(batch)

    except Exception as e:
        # Логируем ошибку, если что-то пошло не так
        logger.error(f"Ошибка в таске generate_recommendation_task: {e}")
        raise self.retry(exc=e)
