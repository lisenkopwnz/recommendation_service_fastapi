from pyspark.sql import SparkSession

from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePySpark
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService
from recommendation.config import settings


@shared_task
def generate_recommendation_task():
    spark = (
        SparkSession.builder
        .appName("MovieRecommendations")  # Имя приложения
        .master("local[*]")  # Использовать все ядра на локальной машине
        .config("spark.executor.memory", "4g")  # Выделить 4 ГБ памяти на executor
        .config("spark.sql.shuffle.partitions", "200")  # Установить 200 партиций для shuffle
        .getOrCreate()  # Создать или получить существующую сессию
    )
    try:
        # Создаём движок
        engine = RecommendationEnginePySpark(spark,settings.file_system_path,20)

        # Создаём сервис и передаём ему движок
        service = RecommendationService(engine)

        result = service.generate_recommendations()

        return result
    finally:
        # Закрываем SparkSession
        spark.stop()
