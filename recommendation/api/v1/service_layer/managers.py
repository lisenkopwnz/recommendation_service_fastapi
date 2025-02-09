from sqlalchemy.orm import Session

from recommendation.api.v1.adapters.database_sql_alchemy import SQLAlchemyRepository
from recommendation.api.v1.adapters.storage_cache_redis import RedisStorage
from recommendation.api.v1.service_layer.database_manager import DataBaseService
from recommendation.api.v1.service_layer.storage_manager import CacheStorageManager


def create_database_manager(db: Session):
    """Функция создания сервиса и низкоуровневой реализации для работы с базой данных."""
    repository = SQLAlchemyRepository(db)
    database_service = DataBaseService(repository)
    return database_service

def create_cache_manager(host, port, new_db, old_db):
    """Функция создания сервиса и низкоуровневой реализации для работы с кешированием."""
    storage = RedisStorage(host=host, port=port, new_db=new_db, old_db=old_db)
    cache_manager = CacheStorageManager(storage)
    return cache_manager
