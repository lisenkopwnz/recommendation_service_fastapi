from typing import Any, List, Dict
from recommendation.storage.cache.cashe_repository import StorageRepository


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

    def bulk_set(self, data: List[Dict[str, Any]]):
        """Сохраняет значение в кеше по указанному ключу.

        Args:

        """
        self.storage.bulk_set(data)
