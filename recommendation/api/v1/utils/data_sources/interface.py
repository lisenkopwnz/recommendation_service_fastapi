from abc import ABC, abstractmethod


class DataSourceABC(ABC):
    """
    Метакласс, реализующий интерфейс для получения данных из внешнего сервиса.
    """
    @abstractmethod
    def read(self):
        """Абстрактный метод который должен быть реализован для получения данных из внещнего сервиса"""
        pass
