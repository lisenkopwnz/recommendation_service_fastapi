from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DatabaseRepository(ABC):
    """
    Абстрактный базовый класс для работы с базой данных.
    """

    @abstractmethod
    async def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
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
    async def get(self, model: Any, primary_key: int):
        """Ищет одну запись по первичному ключу"""
        pass

    @abstractmethod
    async def commit(self):
        """
        Фиксирует (подтверждает) транзакцию.

        Вызывает сохранение всех внесенных изменений в базе данных.
        Используется после выполнения операций вставки, обновления или удаления,
        чтобы изменения стали постоянными.
        """
        pass

    @abstractmethod
    async def rollback(self):
        """
        Отменяет (откатывает) транзакцию.

        Отменяет все изменения, внесенные в рамках текущей транзакции.
        Используется в случае возникновения ошибки или необходимости
        отмены выполненных операций.
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Закрывает соеденение с базой данных выступающей в роли хранилища данных
        """
        pass
