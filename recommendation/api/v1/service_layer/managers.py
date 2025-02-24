from sqlalchemy.ext.asyncio import AsyncSession
from recommendation.api.v1.adapters.database_sql_alchemy import SQLAlchemyRepository
from recommendation.api.v1.adapters.storage_cache_redis import AsyncRedisStorage
from recommendation.api.v1.service_layer.manager_database import DataBaseService
from recommendation.api.v1.service_layer.manager_storage import CacheStorageManager


async def create_async_database_manager(db: AsyncSession) -> DataBaseService:
    """
    Создаёт сервис для работы с базой данных.

    :param db: Асинхронная сессия SQLAlchemy.
    :return: Экземпляр `DataBaseService`.
    """
    repository = SQLAlchemyRepository(db)
    return DataBaseService(repository)


async def create_async_cache_manager(host: str, port: int, new_db: int, old_db: int) -> CacheStorageManager:
    """
    Создаёт сервис для работы с кешированием.

    :param host: Хост Redis.
    :param port: Порт Redis.
    :param new_db: Индекс новой базы Redis.
    :param old_db: Индекс старой базы Redis.
    :return: Экземпляр `CacheStorageManager`.
    """
    storage = AsyncRedisStorage(host=host, port=port, new_db=new_db, old_db=old_db)
    return CacheStorageManager(storage)
