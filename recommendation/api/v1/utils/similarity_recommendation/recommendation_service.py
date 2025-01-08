from recommendation.api.v1.utils.similarity_recommendation.interface import Recommendation
from typing import Any

class RecommendationService(Recommendation):
    """
    Сервис для генерации рекомендаций.

    Этот класс является оберткой вокруг движка рекомендаций (engine), который реализует
    логику генерации рекомендаций. Сервис делегирует вызов метода `generate_recommendations`
    движку и возвращает результат.

    Attributes:
        engine (Any): Движок рекомендаций, который должен реализовывать метод `generate_recommendations`.
    """

    def __init__(self, engine: Any):
        """
        Инициализирует сервис рекомендаций.

        Args:
            engine (Any): Движок рекомендаций, который должен реализовывать метод `generate_recommendations`.
        """
        self.engine = engine

    def generate_recommendations(self) -> Any:
        """
        Генерирует рекомендации с использованием движка.

        Returns:
            Any: Результат выполнения метода `generate_recommendations` движка.
                  Тип возвращаемого значения зависит от реализации движка.
        """
        return self.engine.generate_recommendations()
