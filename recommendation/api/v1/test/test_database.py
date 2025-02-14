from unittest.mock import MagicMock, ANY
import pytest
from sqlalchemy.orm import Session

from recommendation.api.v1.service_layer.manager_database import DataBaseService
from recommendation.api.v1.domain.database_repository import DatabaseRepository
from recommendation.api.v1.adapters.database_sql_alchemy import SQLAlchemyRepository


@pytest.fixture
def mock_repository():
    """
    Фикстура для мокированного репозитория.
    """
    return MagicMock(spec=DatabaseRepository)

def test_bulk_update_calls_repository(mock_repository):
    """
    Проверяет, что метод bulk_update в DataBaseService вызывает метод bulk_update репозитория с правильными параметрами.
    """
    service = DataBaseService(mock_repository)

    query = "UPDATE table SET recommended_ids = :recommended_ids WHERE id = :id"
    params = [
        {"id": 1, "recommended_ids": [101, 102]},
        {"id": 2, "recommended_ids": [103, 104]},
    ]

    result = service.bulk_update(query, params)

    # Проверяем, что метод bulk_update репозитория был вызван с нужными параметрами
    mock_repository.bulk_update.assert_called_with(query, params)

    # Проверяем, что сервис просто возвращает результат метода репозитория
    assert result == mock_repository.bulk_update.return_value

@pytest.fixture
def mock_session():
    """
    Фикстура для мокированной сессии SQLAlchemy.
    """
    return MagicMock(spec=Session)

def test_bulk_update_success(mock_session):
    """
    Проверяет, что SQLAlchemyRepository.bulk_update() выполняет SQL-запрос с нужными параметрами.
    """
    repo = SQLAlchemyRepository(mock_session)

    query = "UPDATE table SET recommended_ids = :recommended_ids WHERE id = :id"
    params = [
        {"id": 1, "recommended_ids": [101, 102]},
        {"id": 2, "recommended_ids": [103, 104]},
    ]

    result = repo.bulk_update(query, params)

    # Проверяем, что транзакция была начата
    mock_session.begin.assert_called_once()

    # Проверяем, что execute вызван с нужными параметрами
    mock_session.execute.assert_called_with(ANY, [
        {"id": 1, "recommended_ids": [101, 102]},
        {"id": 2, "recommended_ids": [103, 104]}
    ])

    # Проверяем, что метод возвращает None при успешном выполнении
    assert result is None

def test_bulk_update_rollback_on_error(mock_session):
    """
    Проверяет, что при ошибке SQLAlchemyRepository.bulk_update() вызывает rollback().
    """
    repo = SQLAlchemyRepository(mock_session)

    query = "UPDATE table SET recommended_ids = :recommended_ids WHERE id = :id"
    params = [{"id": 1, "recommended_ids": [101, 102]}]

    # Настраиваем мок, чтобы session.execute() выбросил исключение
    mock_session.execute.side_effect = Exception("DB Error")

    result = repo.bulk_update(query, params)

    # Проверяем, что rollback был вызван при ошибке
    mock_session.rollback.assert_called_once()

    # Проверяем, что метод вернул словарь с ошибкой
    assert result == {"error": "DB Error"}
