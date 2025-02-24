import os
import aiofiles
from fastapi import UploadFile


class FileHandlerCSV:
    """
    Класс для обработки файлов, включающий создание директорий и асинхронное сохранение файлов на диск.

    Attributes:
        file (UploadFile): Файл, который необходимо сохранить. Это объект UploadFile от FastAPI.
        path_uploaded_data_file (str): Путь, по которому будет сохранён файл на диске.
    """

    def __init__(self, file: UploadFile, path_uploaded_data_file: str) -> None:
        """
        Инициализация объекта для обработки файла.

        Args:
            file (UploadFile): Загружаемый файл.
            path_uploaded_data_file (str): Путь для сохранения файла, включая имя файла и расширение.

        Это также вызывает метод для проверки существования и создания необходимой директории,
        если она не существует.
        """
        self.file = file
        self.path_uploaded_data_file = os.path.join(
            path_uploaded_data_file, file.filename
        )
        self.ensure_directory_exists()

    def ensure_directory_exists(self) -> None:
        """
        Проверяет, существует ли директория для сохранения файла.
        Если её нет, создаёт её.

        Raises:
            RuntimeError: Если не удалось создать директорию (например, из-за проблем с правами доступа).
        """
        try:
            os.makedirs(os.path.dirname(self.path_uploaded_data_file), exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Не удалось создать директорию: {e}")

    async def save_file(self) -> None:
        """
        Асинхронно сохраняет файл на диск. Загружаемый файл сохраняется по указанному пути.

        Файл читается по частям (по 1 МБ), чтобы избежать проблем с памятью при загрузке больших файлов.

        Raises:
            RuntimeError: Если произошла ошибка при записи файла на диск.
        """
        try:
            # Открытие файла для записи в бинарном режиме (wb), чтобы сохранить содержимое.
            async with aiofiles.open(self.path_uploaded_data_file, "wb") as buffer:
                # Чтение файла частями по 1 МБ и запись каждой части в новый файл.
                while chunk := await self.file.read(1024 * 1024):
                    await buffer.write(chunk)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении файла: {e}")
