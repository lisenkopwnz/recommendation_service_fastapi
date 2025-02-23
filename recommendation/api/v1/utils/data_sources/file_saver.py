import os
import aiofiles
from fastapi import UploadFile

from recommendation.api.v1.utils.data_sources.interface import DataSourceABC


class FileHandlerCSV(DataSourceABC):
    """
    Класс для обработки файлов: сохранения на диск и проверки директорий.

    Attributes:
        file: Файл для сохранения. Может быть объектом UploadFile или файловым объектом.
        save_path: Полный путь для сохранения файла.
    """

    def __init__(self, file:UploadFile, save_path: str) -> None:
        self.file = file
        self.save_path = save_path
        self.ensure_directory_exists()

    def ensure_directory_exists(self) -> None:
        """
        Создаёт директорию для сохранения файла, если она не существует.

        Raises:
            RuntimeError: Если не удалось создать директорию.
        """
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Не удалось создать директорию: {e}")

    async def save_file(self) -> None:
        """
        Асинхронно сохраняет файл на диск.

        Raises:
            RuntimeError: Если произошла ошибка при сохранении файла.
        """
        try:
            async with aiofiles.open(self.save_path, "wb") as buffer:
                while chunk := await self.file.read(1024 * 1024):
                    await buffer.write(chunk)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении файла: {e}")
