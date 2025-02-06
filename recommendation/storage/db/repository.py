from abc import ABC, abstractmethod
from typing import Any, Dict, List, Generator


class DatabaseRepository(ABC):
    """
    Абстрактный базовый класс для работы с базой данных.
    """

    @abstractmethod
    def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): Сырой SQL-запрос.
            params (Generator): Генератор, который возвращает данные пакетами.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        pass
