from typing import Any
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

    def set(self, key: str, value: Any):
        """Сохраняет значение в кеше по указанному ключу.

        Args:
            key (str): Ключ для сохранения значения.
            value (Any): Значение, которое нужно сохранить.
        """
        self.storage.set(key, value)
