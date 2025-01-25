from typing import Dict, Any, Generator, List
from recommendation.db.repository import DatabaseRepository


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

    def bulk_update(self, query: str, params: Generator[List[Dict[str, Any]], None, None]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): SQL-запрос.
            params (Generator): Генератор, который возвращает данные пакетами.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        return self.repository.bulk_update(query, params)
