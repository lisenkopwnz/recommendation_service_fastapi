from fastapi import UploadFile
from recommendation.api.v1.utils.data_sources.file_saver import FileHandlerCSV
from recommendation.api.v1.utils.data_sources.interface import DataSourceABC


class FileSaverFactory:
    """
    Фабрика для создания объектов, отвечающих за сохранение файлов в файловую систему.
    """

    @staticmethod
    def get_saver(file: UploadFile, save_path: str) -> DataSourceABC:
        """
        Возвращает подходящий объект для сохранения файла в зависимости от его формата.

        Args:
            file: Файл для сохранения.
            save_path: Путь для сохранения файла.

        Returns:
            FileSaver: Объект, отвечающий за сохранение файла.

        Raises:
            ValueError: Если формат файла не поддерживается.
        """
        if file.filename.endswith(".csv"):
            return FileHandlerCSV(file, save_path)
        else:
            raise ValueError("Формат файла не поддерживается. Поддерживаются только CSV-файлы.")
