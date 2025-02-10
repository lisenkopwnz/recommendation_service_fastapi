from sqlalchemy.ext.asyncio import AsyncSession

from recommendation.api.v1.adapters.database_sql_alchemy import SQLAlchemyRepository
from recommendation.api.v1.adapters.storage_cache_redis import AsyncRedisStorage
from recommendation.api.v1.service_layer.database_manager import DataBaseService
from recommendation.api.v1.service_layer.storage_manager import CacheStorageManager


async def create_async_database_manager(db: AsyncSession):
    """Функция создания сервиса и низкоуровневой реализации для работы с базой данных."""
    repository = SQLAlchemyRepository(db)
    database_service = DataBaseService(repository)
    return database_service

async def create_async_cache_manager(host, port, new_db, old_db):
    """Функция создания сервиса и низкоуровневой реализации для работы с кешированием."""
    storage = AsyncRedisStorage(host=host, port=port, new_db=new_db, old_db=old_db)
    cache_manager = CacheStorageManager(storage)
    return cache_manager
