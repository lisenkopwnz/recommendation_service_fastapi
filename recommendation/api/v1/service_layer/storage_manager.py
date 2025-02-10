from typing import Any, List, Dict

from sqlalchemy.util import await_only

from recommendation.api.v1.domain.cashe_repository import StorageRepository


class CacheStorageManager:
    """Высокоуровневый менеджер для работы с кешированием.

    Абстрагирует логику работы с кешем, предоставляя простой интерфейс для операций.
    """

    def __init__(self, storage: StorageRepository):
        """Инициализирует менеджер с указанным хранилищем.

        Args:
            storage (StorageRepository): Реализация хранилища для кеширования.
        """
        self.storage = storage

    async def bulk_set(self, data: List[Dict[str, Any]]):
        """Сохраняет значение в кеше по указанному ключу.

        Args:

        """
        await self.storage.bulk_set(data)

    async def get(self, key: str):
        """ Получает значение по ключу """
        return await self.storage.get(key)

    async def commit(self):
        """Фиксирует все изменения, внесенные в кеш.

        Вызывает метод commit у используемого хранилища, чтобы сохранить данные в постоянном состоянии.
        """
        return await self.storage.commit()

    async def rollback(self):
        """Отменяет все несохраненные изменения в кеше.

        Вызывает метод rollback у используемого хранилища, чтобы вернуть кеш в предыдущее состояние.
        """
        return await self.storage.rollback()
