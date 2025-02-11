import orjson

from recommendation.api.v1.adapters.dependencies import get_db
from recommendation.api.v1.adapters.models import  SimilarContentRecommendation
from recommendation.api.v1.service_layer.managers import create_async_cache_manager, create_async_database_manager


async def get_similar_videos(id: int):

    db = await get_db()
    database_service = await create_async_database_manager(db)

    cache_manager = await create_async_cache_manager(host='localhost', port=6379, new_db=0, old_db=1)

    # Сначала пытаемся получить данные из кэша
    if arr_videos := await cache_manager.get(f'videos_id:{str(id)}'):
        return orjson.loads(arr_videos)

    # Если нет в кэше, пытаемся получить из базы данных
    elif arr_videos := await database_service.get(SimilarContentRecommendation, id):
        return arr_videos

    # Если не нашли в кэше и базе, возвращаем None
    else:
        return None