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
            params (List[Dict[str, Any]]): Список словарей с параметрами запроса.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        pass

    @abstractmethod
    def commit(self):
        """
        Фиксирует (подтверждает) транзакцию.

        Вызывает сохранение всех внесенных изменений в базе данных.
        Используется после выполнения операций вставки, обновления или удаления,
        чтобы изменения стали постоянными.
        """
        pass

    @abstractmethod
    def rollback(self):
        """
        Отменяет (откатывает) транзакцию.

        Отменяет все изменения, внесенные в рамках текущей транзакции.
        Используется в случае возникновения ошибки или необходимости
        отмены выполненных операций.
        """
        pass
