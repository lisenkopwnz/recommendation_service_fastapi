from abc import ABC, abstractmethod
from typing import Any


class StorageRepository(ABC):
    """Абстрактный класс ,который описывает интерфейс для работы с инструментами кеширования."""

    @abstractmethod
    def set(self,key: str, value: Any):
        """Абстрактный метод ,который описывает добавление строкового значения по ключу."""
        pass
