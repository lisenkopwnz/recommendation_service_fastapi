from typing import Any, List, Dict
from recommendation.api.v1.domain.cashe_repository import StorageRepository


class CacheStorageManager:
    """
    Высокоуровневый менеджер для работы с кешированием.

    Абстрагирует логику работы с кешем, предоставляя простой интерфейс для операций.
    """

    def __init__(self, storage: StorageRepository):
        """
        Инициализирует менеджер с указанным хранилищем.

        :param storage: Реализация хранилища для кеширования.
        """
        self.storage = storage

    async def bulk_set(self, data: List[Dict[str, Any]]) -> None:
        """
        Сохраняет сразу несколько значений в кеше.

        :param data: Список словарей с данными для кеширования.
        """
        await self.storage.bulk_set(data)

    async def get(self, key: str) -> Any:
        """
        Получает значение из кеша по указанному ключу.

        :param key: Ключ, по которому нужно получить данные.
        :return: Значение из кеша или `None`, если данных нет.
        """
        return await self.storage.get(key)

    async def commit(self) -> None:
        """
        Фиксирует все изменения в кеше.

        Вызывает метод `commit` у используемого хранилища, чтобы сохранить данные.
        """
        await self.storage.commit()

    async def rollback(self) -> None:
        """
        Отменяет все несохраненные изменения в кеше.

        Вызывает метод `rollback` у используемого хранилища, чтобы вернуть кеш в предыдущее состояние.
        """
        await self.storage.rollback()

    async def close(self) -> None:
        """
        Закрывает соединение с кешем.

        Вызывает метод `close` у используемого хранилища, чтобы освободить ресурсы.
        """
        await self.storage.close()
