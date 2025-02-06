from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StorageRepository(ABC):
    """Абстрактный класс ,который описывает интерфейс для работы с инструментами кеширования."""

    @abstractmethod
    def bulk_set(self, data: List[Dict[str, Any]]):
        """Абстрактный метод ,который описывает массовое добавление строкового значения по ключу."""
        pass
