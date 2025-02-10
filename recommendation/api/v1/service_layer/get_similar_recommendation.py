import orjson
from sqlalchemy.orm import Session

from recommendation.api.v1.service_layer.managers import create_database_manager, create_cache_manager
from recommendation.api.v1.adapters.models import SessionLocal, SimilarContentRecommendation


def get_similar_videos(id: int):
    database_service = create_database_manager(db)

    cache_manager = create_cache_manager(host='localhost', port=6379, new_db=0, old_db=1)

    # Сначала пытаемся получить данные из кэша
    if arr_videos := cache_manager.get(f'videos_id:{str(id)}'):
        return orjson.loads(arr_videos)

    # Если нет в кэше, пытаемся получить из базы данных
    elif arr_videos := database_service.get(SimilarContentRecommendation, id):
        return arr_videos

    # Если не нашли в кэше и базе, возвращаем None
    else:
        return None