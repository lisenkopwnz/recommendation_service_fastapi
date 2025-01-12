from typing import Dict, Any

from recommendation.db.repository import DatabaseRepository


class DataBaseService(DatabaseRepository):
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

    def bulk_update(self, query: str, params: Dict[str, Any]) -> None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): Сырой SQL-запрос.
            params (Dict[str, Any]): Параметры для запроса.
        """
        self.repository.bulk_update(query, params)