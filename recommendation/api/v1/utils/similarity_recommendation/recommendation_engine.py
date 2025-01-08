from pyspark.pandas import DataFrame
from pyspark.sql.connect.functions import concat_ws

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, Normalizer
from pyspark.sql.functions import col, coalesce, lit, concat_ws
from pyspark.sql.types import FloatType
from pyspark.ml.linalg import DenseVector
import numpy as np

from recommendation.api.v1.utils.similarity_recommendation.interface import Recommendation
from recommendation.config import settings

class RecommendationEnginePySpark(Recommendation):
    """
    Движок для генерации рекомендаций на основе текстовых данных с использованием PySpark.

    Основные шаги:
    1. Загрузка данных из CSV.
    2. Подготовка текстовых данных (токенизация, TF-IDF, нормализация).
    3. Вычисление косинусного сходства между элементами.
    4. Генерация рекомендаций для каждого элемента.
    """

    def __init__(self, spark: SparkSession, path: str, top_n: int):
        """
        Инициализация движка рекомендаций.

        :param spark: Сессия Spark.
        :param path: Путь к CSV-файлу с данными.
        :param top_n: Количество рекомендаций для каждого элемента.
        """
        self.spark = spark
        self.path = path
        self.top_n = top_n

    @staticmethod
    def _cosine_similarity(v1: DenseVector, v2: DenseVector) -> float:
        """
            Вычисляет косинусное сходство между двумя векторами.

            :param v1: Первый вектор.
            :param v2: Второй вектор.
            :return: Косинусное сходство (float).
        """
        # Преобразуем DenseVector в массивы NumPy
        v1_array = v1.toArray()
        v2_array = v2.toArray()

        # Вычисляем косинусное сходство
        dot_product = np.dot(v1_array, v2_array)
        norm_v1 = np.linalg.norm(v1_array)
        norm_v2 = np.linalg.norm(v2_array)

        # Возвращаем косинусное сходство
        return float(dot_product / (norm_v1 * norm_v2))

    def generate_recommendations(self) -> DataFrame:
        """
        Генерирует рекомендации для всех элементов в данных.

        :return: DataFrame с колонками:
                 - id: Идентификатор элемента.
                 - recommended_ids: Список рекомендованных идентификаторов.
        """
        cosine_similarity_udf = self.spark.udf.register(
            "cosine_similarity", RecommendationEnginePySpark._cosine_similarity, FloatType()
        )

        normalized_data = self._prepare_for_cosine_similarity()

        recommendations_df = normalized_data.select("id").distinct().rdd.map(
            lambda row: (row["id"], self._get_top_recommendations(
                item_id=row["id"],
                top_n=self.top_n,
                normalized_data=normalized_data,
                cosine_similarity_udf=cosine_similarity_udf
            ))
        ).toDF(["id", "recommended_ids"])

        return recommendations_df

    @staticmethod
    def _get_top_recommendations(item_id: int, top_n: int, normalized_data, cosine_similarity_udf):
        """
            Возвращает топ-N рекомендаций для указанного элемента.

            :param item_id: Идентификатор элемента.
            :param top_n: Количество рекомендаций.
            :param normalized_data: DataFrame с нормализованными векторами.
            :param cosine_similarity_udf: UDF для вычисления косинусного сходства.
            :return: Список идентификаторов рекомендованных элементов.
        """
        # Получение вектора целевого элемента
        target_item = normalized_data.filter(col("id") == item_id).select("norm_features").collect()[0][0]

        # Вычисление сходства и получение рекомендаций
        recommendations = (((((normalized_data
                           .withColumn("similarity", cosine_similarity_udf(col("norm_features"), lit(target_item))))
                           .filter(col("id") != item_id))
                           .orderBy(col("similarity").desc()))
                           .select("id"))
                           .limit(top_n))

        return recommendations.select("id").rdd.flatMap(lambda x: x).collect()

    def _prepare_for_cosine_similarity(self)-> DataFrame:
        """
            Подготавливает данные для вычисления косинусного сходства.

            :return: DataFrame с нормализованными векторами.
        """
        df = self.uploading_data()  # Загрузка данных
        df = RecommendationEnginePySpark._check_required_columns(df)  # Проверка наличия всех необходимых колонок
        df = RecommendationEnginePySpark._default_empty_strings(df)  # Заполнение пустых значений в текстовых колонках
        df = RecommendationEnginePySpark._combine_text_columns(df)  # Объединение текстовых данных (описание, категории, теги) в одну колонку
        normalized_data = RecommendationEnginePySpark._transform_text_to_tfidf(df)
        return normalized_data

    def uploading_data(self) -> DataFrame:
        """
        Загружает данные из CSV-файла.

        :return: DataFrame с загруженными данными.
        """
        df = self.spark.read.csv(self.path, header=True, inferSchema=True)
        return df

    @staticmethod
    def _check_required_columns(df: DataFrame):
        """
        Проверяет наличие обязательных колонок в DataFrame.

        :param df: DataFrame для проверки.
        :raises ValueError: Если отсутствуют обязательные колонки.
        """
        required_columns = settings
        if not all(column in df.columns for column in required_columns):
            raise ValueError(
                "CSV должен содержать колонки: id, title, description, rating, pub_date, categories, tags"
            )

    @staticmethod
    def _default_empty_strings(df: DataFrame) -> DataFrame:
        """
        Заменяет null в текстовых колонках на пустые строки.

        :param df: Входной DataFrame.
        :return: DataFrame с замененными значениями.
        """
        df = (
            df.withColumn("title", coalesce(col("title"), lit("")))
            .withColumn("description", coalesce(col("description"), lit("")))
            .withColumn("categories", coalesce(col("categories"), lit("")))
            .withColumn("tags", coalesce(col("tags"), lit("")))
        )
        return df

    @staticmethod
    def _combine_text_columns(df: DataFrame) -> DataFrame:
        """
        Объединяет текстовые колонки в одну.

        :param df: Входной DataFrame.
        :return: DataFrame с новой колонкой `text_data`.
        """
        df = df.withColumn(
            "text_data",
            concat_ws(" ", col("title"), col("description"), col("categories"), col("tags"))
        )
        return df

    @staticmethod
    def _transform_text_to_tfidf(df: DataFrame) -> DataFrame:
        """
        Преобразует текстовые данные в числовые векторы с использованием TF-IDF и нормализует их.

        :param df: DataFrame с текстовыми данными.
        :return: DataFrame с нормализованными векторами.
        """
        tokenizer = Tokenizer(inputCol="text_data", outputCol="words")
        words_data = tokenizer.transform(df)

        hashing_tf = HashingTF(inputCol="words", outputCol="raw_features", numFeatures=5000)
        featurized_data = hashing_tf.transform(words_data)

        idf = IDF(inputCol="raw_features", outputCol="features")
        idf_model = idf.fit(featurized_data)
        rescaled_data = idf_model.transform(featurized_data)

        normalizer = Normalizer(inputCol="features", outputCol="norm_features", p=2)
        normalized_data = normalizer.transform(rescaled_data)

        return normalized_data
