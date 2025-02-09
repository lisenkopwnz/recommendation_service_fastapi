from typing import Dict, Any, Generator, List

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

    def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): SQL-запрос.
            params (Generator): Генератор, который возвращает данные пакетами.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        return self.repository.bulk_update(query, params)

    def get(self, model: Any, key: Any):
        """Получает запись"""
        return self.repository.get(model,key)

    def commit(self):
        """ Выполняет фиксацию транзакции """
        return self.repository.commit()

    def rollback(self):
        """ Выполняет откат транзакции """
        return self.repository.rollback()
