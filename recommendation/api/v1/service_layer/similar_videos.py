import logging
import orjson
from recommendation.api.v1.adapters.dependencies import get_db
from recommendation.api.v1.adapters.models import SimilarContentRecommendation, RecommendationResponse
from recommendation.api.v1.service_layer.managers import create_async_cache_manager, create_async_database_manager
from recommendation.config import settings

logger = logging.getLogger(__name__)

async def get_similar_videos(video_id: int) -> list[int] | None:
    """
    Получает похожие видео по `video_id`.

    1. Проверяет кеш Redis.
    2. Если данных нет, загружает их из базы данных.
    3. Если данных нет в базе, возвращает None.

    :param video_id: ID видео, для которого ищем рекомендации.
    :return: Список ID похожих видео или None, если данных нет.
    """

    # Создаём менеджер кэша Redis
    cache_manager = await create_async_cache_manager(
        host=settings.redis_host,
        port=settings.redis_port,
        new_db=settings.new_db,
        old_db=settings.old_db
    )

    # Проверяем кэш в Redis
    if videos := await cache_manager.get(f'videos_id:{str(video_id)}'):
        logger.info(f"Данные из кэша: {videos}")
        return orjson.loads(videos)  # Десериализуем JSON и возвращаем список

    # Если данных нет в кэше, создаём менеджер базы данных
    db = await get_db()
    database_service = await create_async_database_manager(db)

    # Запрашиваем данные из БД
    if videos := await database_service.get(SimilarContentRecommendation, video_id):
        logger.info(f"Данные из БД: {videos.recommendation_id}")
        return videos.recommendation_id  # Возвращаем список рекомендаций из ORM-модели

    # Если данных нет ни в кэше, ни в базе — возвращаем None
    return None
