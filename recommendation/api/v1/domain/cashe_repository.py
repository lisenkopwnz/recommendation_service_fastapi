from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StorageRepository(ABC):
    """Абстрактный класс ,который описывает интерфейс для работы с инструментами кеширования."""

    @abstractmethod
    def bulk_set(self, data: List[Dict[str, Any]]):
        """Абстрактный метод ,который описывает массовое добавление строкового значения по ключу."""
        pass

    @abstractmethod
    def get(self, key: str):
        """Абстрактный метод для получения записи по ключу"""
        pass

    @abstractmethod
    def commit(self):
        """Aбстрактный метод для фиксации изменений после выполнения транзакции в базе данных"""
        pass

    @abstractmethod
    def rollback(self):
        """Aбстрактный метод для отката изменений в случае ошибки в базе данных"""
        pass
