from fastapi import UploadFile
from recommendation.api.v1.service_layer.file_storage.file_saver import FileHandlerCSV


class FileSaverFactory:
    """
    Фабрика для создания объектов, отвечающих за сохранение файлов в файловую систему.
    """

    @staticmethod
    def get_saver(file: UploadFile, path_uploaded_data_file: str):
        """
        Возвращает подходящий объект для сохранения файла в зависимости от его формата.

        Args:
            file: Файл для сохранения.
            path_uploaded_data_file: Путь для сохранения файла.

        Returns:
            FileSaver: Объект, отвечающий за сохранение файла.

        Raises:
            ValueError: Если формат файла не поддерживается.
        """
        if file.filename.endswith(".csv"):
            return FileHandlerCSV(file, path_uploaded_data_file)
        else:
            raise ValueError("Формат файла не поддерживается.")
