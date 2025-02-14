from typing import Dict, Any, List

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
