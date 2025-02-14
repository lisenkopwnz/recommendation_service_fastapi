from unittest.mock import patch, AsyncMock

import pytest
from starlette.datastructures import UploadFile

from recommendation.api.v1.service_layer.event_handlers import generate_recommendations_handler, save_file_handler
from recommendation.api.v1.service_layer.task import generate_recommendation_task
from recommendation.api.v1.utils.data_sources.factory_saver import FileSaverFactory


@pytest.mark.asyncio
async def test_generate_recommendation_handler():
    # Мокируем задачу Celery
    with patch.object(generate_recommendation_task, 'delay') as mock_delay:
        # Вызов обработчика
        await generate_recommendations_handler()
        # Проверка, что метод delay был вызван
        mock_delay.assert_called_once()

@pytest.mark.asyncio
async def test_save_file_handler():
    # Создаем моковый файл (имитация UploadFile)
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test_file.txt"

    file_path = "/fake/path/test_file.txt"

    # Создаем мок для фабрики и для метода save_file()
    mock_saver = AsyncMock()
    with patch.object(FileSaverFactory, 'get_saver', return_value=mock_saver):
        # Вызываем тестируемую функцию
        await save_file_handler(mock_file, file_path)

        # Проверяем, что фабрика вызвана с правильными аргументами
        FileSaverFactory.get_saver.assert_called_once_with(mock_file, file_path)

        # Проверяем, что метод save_file действительно был вызван
        mock_saver.save_file.assert_awaited_once()