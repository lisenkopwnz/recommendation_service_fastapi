import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict


class RecommendationEnginePandas:
    """
    Рекомендательный движок, который генерирует рекомендации на основе текстовых данных.

    Использует TF-IDF для векторного представления текста и косинусное сходство
    для вычисления схожести между элементами.

    Attributes:
        path (str): Путь к CSV-файлу с данными.
        top_n (int): Количество рекомендаций для каждого элемента.
    """

    def __init__(self, path: str, top_n: int):
        """
        Инициализирует RecommendationEnginePandas.

        Args:
            path (str): Путь к CSV-файлу с данными.
            top_n (int): Количество рекомендаций для каждого элемента.
        """
        self.path = path
        self.top_n = top_n

    def generate_recommendations(self) -> pd.DataFrame:
        """
        Генерирует рекомендации для всех элементов в данных.

        Returns:
            pd.DataFrame: DataFrame с колонками:
                - id: Идентификатор элемента.
                - recommended_ids: Список рекомендованных идентификаторов.
        """
        df = self._upload_data()
        df = self._prepare_for_cosine_similarity(df)
        similarity_matrix = RecommendationEnginePandas._calculate_similarity_matrix(df)
        recommendations_df = RecommendationEnginePandas._get_top_recommendations_from_matrix(
            similarity_matrix, df, self.top_n
        )
        return recommendations_df

    def _upload_data(self) -> pd.DataFrame:
        """
        Загружает данные из CSV-файла.

        Returns:
            pd.DataFrame: DataFrame с загруженными данными.
        """
        return pd.read_csv(self.path)

    def _prepare_for_cosine_similarity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Подготавливает данные для вычисления косинусного сходства.

        Args:
            df (pd.DataFrame): Входной DataFrame.

        Returns:
            pd.DataFrame: DataFrame с колонками "id" и "text_data".
        """
        df = self._check_required_columns(df)
        df = self._fill_empty_strings(df)
        df = self._combine_text_columns(df)
        return df

    @staticmethod
    def _check_required_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Проверяет наличие обязательных колонок в DataFrame.

        Args:
            df (pd.DataFrame): DataFrame для проверки.

        Raises:
            ValueError: Если отсутствуют обязательные колонки.

        Returns:
            pd.DataFrame: Проверенный DataFrame.
        """
        required_columns = ["id", "title", "description", "categories", "tags"]
        if not all(column in df.columns for column in required_columns):
            raise ValueError(
                "CSV должен содержать колонки: id, title, description, categories, tags"
            )
        return df

    @staticmethod
    def _fill_empty_strings(df: pd.DataFrame) -> pd.DataFrame:
        """
        Заменяет NaN в текстовых колонках на пустые строки.

        Args:
            df (pd.DataFrame): Входной DataFrame.

        Returns:
            pd.DataFrame: DataFrame с заполненными пустыми значениями.
        """
        text_columns = ["title", "description", "categories", "tags"]
        df[text_columns] = df[text_columns].fillna("")
        return df

    @staticmethod
    def _combine_text_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Объединяет текстовые колонки в одну колонку `text_data`.

        Args:
            df (pd.DataFrame): Входной DataFrame.

        Returns:
            pd.DataFrame: DataFrame с новой колонкой `text_data`.
        """
        df["text_data"] = (
            df["title"] + " " + df["description"] + " " + df["categories"] + " " + df["tags"]
        )
        return df

    @staticmethod
    def _calculate_similarity_matrix(df: pd.DataFrame) -> np.ndarray:
        """
        Вычисляет матрицу сходства между элементами на основе текстовых данных.

        Args:
            df (pd.DataFrame): DataFrame с колонкой `text_data`.

        Returns:
            np.ndarray: Матрица сходства (N x N), где N — количество элементов.
        """
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf_vectorizer.fit_transform(df["text_data"])
        return cosine_similarity(tfidf_matrix, tfidf_matrix)

    @staticmethod
    def _get_top_recommendations_from_matrix(
        similarity_matrix: np.ndarray, df: pd.DataFrame, top_n: int
    ) -> pd.DataFrame:
        """
        Выбирает топ-N рекомендаций для каждого элемента из матрицы сходства.

        Args:
            similarity_matrix (np.ndarray): Матрица сходства.
            df (pd.DataFrame): DataFrame с оригинальными данными.
            top_n (int): Количество рекомендаций.

        Returns:
            pd.DataFrame: DataFrame с колонками:
                - id: Идентификатор элемента.
                - recommended_ids: Список рекомендованных идентификаторов.
        """
        recommendations = defaultdict(list)
        num_items = similarity_matrix.shape[0]

        for i in range(num_items):
            similarity_scores = list(enumerate(similarity_matrix[i]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            top_recommendations = [df.iloc[j]["id"] for j, _ in similarity_scores[1 : top_n + 1]]
            recommendations[df.iloc[i]["id"]] = top_recommendations

        return pd.DataFrame(list(recommendations.items()), columns=["id", "recommended_ids"])
