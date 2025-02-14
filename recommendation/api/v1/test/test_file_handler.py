import pytest
from unittest.mock import patch, AsyncMock
from fastapi import UploadFile
from io import BytesIO
from recommendation.api.v1.utils.data_sources.file_saver import FileHandlerCSV
from recommendation.logging_config import setup_logger

logger = setup_logger()

@pytest.mark.asyncio
async def test_ensure_directory_exists():
    file_content = b"test data"
    file_like = BytesIO(file_content)
    upload_file = UploadFile(file=file_like, filename="test.txt")

    with patch("os.makedirs") as mock_makedirs:
        file_handler = FileHandlerCSV(file=upload_file, save_path="/path/to/save/test.txt")

        mock_makedirs.assert_called_once_with("/path/to/save", exist_ok=True)

@pytest.mark.asyncio
async def test_ensure_directory_exists_failure():
    file_content = b"test data"
    file_like = BytesIO(file_content)
    upload_file = UploadFile(file=file_like, filename="test.txt")

    with patch("os.makedirs", side_effect=OSError("Ошибка создания директории")):
        with pytest.raises(RuntimeError, match="Не удалось создать директорию: Ошибка создания директории"):
            FileHandlerCSV(file=upload_file, save_path="/path/to/save/test.txt")

@pytest.mark.asyncio
async def test_save_file():
    file_content = b"test data"
    file_like = BytesIO(file_content)

    upload_file = UploadFile(file=file_like, filename="test.txt")

    mock_file = AsyncMock()
    mock_file.__aenter__.return_value.write = AsyncMock()

    with patch("aiofiles.open", return_value=mock_file):
        file_handler = FileHandlerCSV(file=upload_file, save_path="/path/to/save/test.txt")

        await file_handler.save_file()
        mock_file.__aenter__.return_value.write.assert_called_once_with(b"test data")

@pytest.mark.asyncio
async def test_save_file_failure():
    # Создаём фиктивный файловый объект
    file_content = b"test data"
    file_like = BytesIO(file_content)

    upload_file = UploadFile(file=file_like, filename="test.txt")

    mock_file = AsyncMock()
    mock_file.__aenter__.side_effect = Exception("Ошибка записи")

    with patch("aiofiles.open", return_value=mock_file):
        file_handler = FileHandlerCSV(file=upload_file, save_path="/path/to/save/test.txt")

        with pytest.raises(RuntimeError, match="Ошибка при сохранении файла: Ошибка записи"):
            await file_handler.save_file()
