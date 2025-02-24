from typing import Dict, Any, List
import pandas as pd
from recommendation.api.v1.domain.database_repository import DatabaseRepository


class DataBaseService:
    """
    Высокоуровневый сервис для работы с базой данных.
    """

    def __init__(self, repository: DatabaseRepository):
        """
        Инициализирует сервис с переданным репозиторием базы данных.

        :param repository: Экземпляр `DatabaseRepository` для работы с БД.
        """
        self.repository = repository

    async def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление записей в базе данных.

        :param query: SQL-запрос для выполнения.
        :param params: Список параметров для массового обновления.
        :return: Результат операции в виде `Dict`, либо `None` в случае успеха.
        """
        return await self.repository.bulk_update(query, params)

    def batch_generator(self, df: pd.DataFrame, batch_size: int = 1000):
        """
        Разбивает `DataFrame` на батчи заданного размера.

        :param df: `pandas.DataFrame`, который нужно разбить.
        :param batch_size: Размер одной партии (по умолчанию 1000).
        :return: Генератор батчей данных.
        :raises NotImplementedError: Если метод `batch_generator` не реализован в репозитории.
        """
        if hasattr(self.repository, 'batch_generator'):
            return self.repository.batch_generator(df, batch_size)
        raise NotImplementedError("Метод `batch_generator` не реализован в репозитории.")

    async def get(self, model: Any, key: Any) -> Any:
        """
        Получает запись из базы данных по ключу.

        :param model: ORM-модель, в которой выполняется поиск.
        :param key: Значение первичного ключа для поиска.
        :return: Найденная запись или `None`, если запись не найдена.
        """
        return await self.repository.get(model, key)

    async def commit(self) -> None:
        """
        Фиксирует изменения в базе данных.
        """
        await self.repository.commit()

    async def rollback(self) -> None:
        """
        Откатывает незавершённые изменения в базе данных.
        """
        await self.repository.rollback()

    async def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        await self.repository.close()
