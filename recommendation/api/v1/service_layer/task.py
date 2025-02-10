from celery import shared_task
from celery.utils.log import get_task_logger
import asyncio

from recommendation.api.v1.adapters.dependencies import get_db
from recommendation.api.v1.common.unit_of_work import AsyncUnitOfWork
from recommendation.api.v1.service_layer.managers import create_async_database_manager, create_async_cache_manager
from recommendation.config import settings
from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePandas
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService


logger = get_task_logger(__name__)

async def async_save_to_db_and_cache(result):
    """
    Асинхронная функция для сохранения данных в базу данных и кэш.
    """
    db = await get_db()
    try:
        # Создаем асинхронные клиенты для БД и кеша
        database_service = await create_async_database_manager(db)
        cache_manager = await create_async_cache_manager(host = 'localhost', port = 6379, new_db = 0, old_db = 1)

        # Оборачиваем в UnitOfWork
        async with AsyncUnitOfWork(database_service, cache_manager) as uow:
            batch_gen = database_service.batch_generator(result, batch_size=1000)

            for batch in batch_gen:
                await database_service.bulk_update(
                    query="""
                        INSERT INTO similar_recommendation (id, recommendation_id) 
                        VALUES (:id, :recommended_ids) 
                        ON CONFLICT (id) DO UPDATE SET
                            recommendation_id = EXCLUDED.recommendation_id;
                    """,
                    params=batch
                )
                await cache_manager.bulk_set(batch)

        logger.info("Рекомендации успешно сохранены в БД и кэш.")

    except Exception as e:
        logger.error(f"Ошибка при сохранении данных в БД и кэш: {e}")
        raise

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def generate_recommendation_task(self):
    """
    Синхронная Celery-таска:
    1. Генерирует рекомендации (синхронно).
    2. Вызывает асинхронную функцию для сохранения в БД и кэш.
    """
    try:
        # 1. Генерация рекомендаций (синхронно)
        engine = RecommendationEnginePandas(settings.file_system_path, 20)
        service = RecommendationService(engine)
        result = service.generate_recommendations()

        # 2. Запускаем асинхронное сохранение в фоне с использованием уже активного event loop
        loop = asyncio.get_event_loop()
        loop.create_task(async_save_to_db_and_cache(result))  # Не блокирует основной процесс

    except Exception as e:
        logger.error(f"Ошибка в Celery-таске: {e}")
        raise self.retry(exc=e)
