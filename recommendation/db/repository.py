from abc import ABC, abstractmethod
from typing import Any, Dict


class DatabaseRepository(ABC):
    """
        Абстрактный базовый класс для работы с базой данных.
    """
    @abstractmethod
    def bulk_update(self, query: str, params: Dict[str, Any]) -> None:
        """
                Выполняет массовое обновление данных с использованием сырого SQL-запроса.

                Args:
                    query (str): Сырой SQL-запрос.
                    params (Dict[str, Any]): Параметры для запроса.
        """
        pass