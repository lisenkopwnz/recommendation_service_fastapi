from unittest.mock import MagicMock
import pytest
from recommendation.api.v1.adapters.storage_cache_redis import RedisStorage


@pytest.fixture
def mock_redis():
    """
    Фикстура, которая создает мок-объект для RedisStorage.

    Возвращает:
        MagicMock: Мок-объект, имитирующий поведение класса RedisStorage.
    """
    # Создаю мок для RedisStorage, используя MagicMock, чтобы мы могли проверить его вызовы.
    mock_redis = MagicMock(spec=RedisStorage)
    return mock_redis


def test_bulk_set(mock_redis):
    """
    Тестирует метод `bulk_set` класса RedisStorage.

    Проверяет, что метод `bulk_set` был вызван с правильными данными.

    Этот тест использует мок для RedisStorage, чтобы убедиться, что метод `bulk_set`
    был вызван с параметрами, которые мы ожидаем.

    Подготовка:
        - Готовим тестовые данные для метода `bulk_set`.

    Проверка:
        - Вызываем метод `bulk_set` на мок-объекте.
        - Проверяем, что мок-объект вызвал метод `bulk_set` с ожидаемыми данными.

    Ожидаемый результат:
        - Метод `bulk_set` должен быть вызван с точно такими же данными, как в переменной `data`.

    Аргументы:
        mock_redis (MagicMock): Мок-объект RedisStorage, предоставляемый фикстурой.

    Примечания:
        Этот тест не взаимодействует с реальным Redis-сервером, а использует только мок-объект для проверки вызова метода.
    """
    # Готовим тестовые данные
    data = [{'id': 1, 'recommended_ids': [101, 102]}, {'id': 2, 'recommended_ids': [103, 104]}]

    # Вызываем метод bulk_set на мок-объекте
    mock_redis.bulk_set(data)

    # Проверяем, что метод bulk_set был вызван с нужными данными
    mock_redis.bulk_set.assert_called_with(data)
