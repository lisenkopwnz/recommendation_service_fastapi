import pytest
import pandas as pd
import numpy as np
from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import (
    RecommendationEnginePandas,
)


@pytest.fixture
def sample_data():
    """
    Фикстура, возвращающая тестовый DataFrame с данными для рекомендаций.

    Returns:
        pd.DataFrame: Тестовые данные с колонками id, title, description, categories, tags.
    """
    data = {
        "id": [1, 2, 3],
        "title": ["Title A", "Title B", "Title C"],
        "description": ["Description A", "Description B", "Description C"],
        "categories": ["Category A", "Category B", "Category C"],
        "tags": ["Tag A", "Tag B", "Tag C"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def recommendation_engine(tmp_path, sample_data):
    """
    Фикстура, создающая экземпляр RecommendationEnginePandas с тестовыми данными.

    Args:
        tmp_path: Временный путь для создания файла (предоставляется pytest).
        sample_data: Тестовый DataFrame.

    Returns:
        RecommendationEnginePandas: Экземпляр движка рекомендаций.
    """
    # Сохраняем тестовые данные во временный CSV-файл
    path = tmp_path / "test_data.csv"
    sample_data.to_csv(path, index=False)
    return RecommendationEnginePandas(str(path), top_n=2)


def test_upload_data(recommendation_engine, sample_data):
    """
    Тестирует метод загрузки данных.

    Проверяет, что данные загружаются корректно и соответствуют ожидаемым.
    """
    df = recommendation_engine._upload_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert df.equals(sample_data)


def test_check_required_columns(recommendation_engine, sample_data):
    """
    Тестирует проверку наличия обязательных колонок.

    Проверяет, что все обязательные колонки присутствуют в DataFrame.
    """
    df = recommendation_engine._check_required_columns(sample_data)
    required_columns = ["id", "title", "description", "categories", "tags"]
    assert all(column in df.columns for column in required_columns)


def test_fill_empty_strings(recommendation_engine, sample_data):
    """
    Тестирует замену пустых значений на пустые строки.

    Проверяет, что NaN в текстовых колонках заменяются на пустые строки.
    """
    sample_data.loc[0, "title"] = None
    df = recommendation_engine._fill_empty_strings(sample_data)
    assert df.loc[0, "title"] == ""


def test_combine_text_columns(recommendation_engine, sample_data):
    """
    Тестирует объединение текстовых колонок в одну.

    Проверяет, что колонка `text_data` создается и содержит корректные данные.
    """
    df = recommendation_engine._combine_text_columns(sample_data)
    assert "text_data" in df.columns
    assert df.loc[0, "text_data"] == "Title A Description A Category A Tag A"


def test_calculate_similarity_matrix(recommendation_engine, sample_data):
    """
    Тестирует расчет матрицы сходства.

    Проверяет, что матрица сходства имеет правильную форму и тип.
    """
    df = recommendation_engine._prepare_for_cosine_similarity(sample_data)
    similarity_matrix = recommendation_engine._calculate_similarity_matrix(df)
    assert isinstance(similarity_matrix, np.ndarray)
    assert similarity_matrix.shape == (3, 3)


def test_get_top_recommendations_from_matrix(recommendation_engine, sample_data):
    """
    Тестирует выбор топ-N рекомендаций из матрицы сходства.

    Проверяет, что рекомендации имеют правильный формат и количество.
    """
    df = recommendation_engine._prepare_for_cosine_similarity(sample_data)
    similarity_matrix = recommendation_engine._calculate_similarity_matrix(df)
    recommendations_df = recommendation_engine._get_top_recommendations_from_matrix(
        similarity_matrix, df, top_n=2
    )
    assert isinstance(recommendations_df, pd.DataFrame)
    assert len(recommendations_df) == 3
    assert all(
        len(recommendations_df.loc[i, "recommended_ids"]) == 2
        for i in range(len(recommendations_df))
    )


def test_generate_recommendations(recommendation_engine):
    """
    Тестирует генерацию рекомендаций.

    Проверяет, что метод generate_recommendations возвращает корректный DataFrame.
    """
    recommendations_df = recommendation_engine.generate_recommendations()
    assert isinstance(recommendations_df, pd.DataFrame)
    assert len(recommendations_df) == 3
    assert all(
        len(recommendations_df.loc[i, "recommended_ids"]) == 2
        for i in range(len(recommendations_df))
    )
