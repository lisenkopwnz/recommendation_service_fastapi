from typing import Dict, Any, List

import pandas

from recommendation.api.v1.domain.database_repository import DatabaseRepository


class DataBaseService:
    """
    Высокоуровневый сервис для работы с базой данных.
    """

    def __init__(self, repository: DatabaseRepository):
        """
        Инициализирует сервис.

        Args:
            repository (DatabaseRepository): Репозиторий для работы с базой данных.
        """
        self.repository = repository

    async def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): SQL-запрос.
            params (List[Dict[str, Any]]): Список данных для массового обновления.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        return await self.repository.bulk_update(query, params)

    def batch_generator(self, df: pandas.DataFrame, batch_size: int = 1000):
        """
        Перенаправляет вызов к методу batch_generator из репозитория.
        """
        if hasattr(self.repository, 'batch_generator'):
            return self.repository.batch_generator(df, batch_size)
        else:
            raise NotImplementedError("batch_generator не реализован в репозитории.")

    async def get(self, model: Any, key: Any):
        """Получает запись по ключу"""
        return await self.repository.get(model, key)

    async def commit(self):
        """ Выполняет фиксацию транзакции """
        return await self.repository.commit()

    async def rollback(self):
        """ Выполняет откат транзакции """
        return await self.repository.rollback()

    async def close(self):
        """ Выполняет закрытие соеденения """
        return await self.repository.close()
