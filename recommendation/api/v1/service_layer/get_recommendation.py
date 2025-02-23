import logging
from datetime import datetime

import orjson

from recommendation.api.v1.adapters.dependencies import get_db
from recommendation.api.v1.adapters.models import  SimilarContentRecommendation
from recommendation.api.v1.service_layer.managers import create_async_cache_manager, create_async_database_manager

logger = logging.getLogger(__name__)

async def get_similar_videos(id: int):

    db = await get_db()
    database_service = await create_async_database_manager(db)
    logger.info('1212')

    cache_manager = await create_async_cache_manager(host = 'redis', port = 6379, new_db = 0, old_db = 1)
    logger.info(cache_manager)
    # Сначала пытаемся получить данные из кэша

    arr_videos = await cache_manager.get(f'videos_id:{str(id)}')
    logger.info(arr_videos)
    logger.info(f'videos_id:{str(id)}')
    if arr_videos := await cache_manager.get(f'videos_id:{str(id)}'):
        logger.info(arr_videos)
        return orjson.loads(arr_videos)

    # Если нет в кэше, пытаемся получить из базы данных
    elif arr_videos := await database_service.get(SimilarContentRecommendation, id):
        logger.info(arr_videos)
        return {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in arr_videos.__dict__.items()
            if not key.startswith('_')
        }

    # Если не нашли в кэше и базе, возвращаем None
    else:
        return None