from abc import abstractmethod, ABC


class Recommendation(ABC):
    """
    Абстрактный базовый класс для движка рекомендаций.

    Все классы, реализующие этот интерфейс, должны реализовать метод `generate_recommendations`.
    """
    @abstractmethod
    def generate_recommendations(self):
        """
        Генерирует рекомендации на основе входных данных.

        Returns:
            DataFrame: DataFrame с рекомендациями. Структура DataFrame зависит от реализации.
        """
        pass