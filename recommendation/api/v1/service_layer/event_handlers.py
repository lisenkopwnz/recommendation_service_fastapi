import multiprocessing
import signal

from recommendation.api.v1.service_layer.task import generate_recommendation_task, error_handler
from recommendation.api.v1.utils.data_sources.factory_saver import FileSaverFactory


async def generate_recommendations_handler():
    """
    Обработчик события для генерации рекомендаций.

    Эта функция вызывает асинхронную задачу `generate_recommendation_task`, которая
    добавляется в очередь Celery для выполнения. После того как задача будет выполнена,
    она сгенерирует рекомендации для дальнейшего использования в системе.

    Задача выполняется асинхронно, и обработчик не блокирует выполнение других операций
    приложения.
    """
    signal.signal(signal.SIGUSR1, error_handler)
    process = multiprocessing.Process(target=generate_recommendation_task)
    process.daemon = True
    process.start()

async def save_file_handler(file, file_path):
    """
    Обработчик события для сохранения файла.

    Эта функция получает файл и путь, по которому файл должен быть сохранен в
    файловой системе. Функция использует `FileSaverFactory`, чтобы выбрать подходящий
    механизм сохранения файла в зависимости от типа источника данных.

    Параметры:
        file (UploadFile): Загружаемый файл, который нужно сохранить.
        file_path (str): Путь, по которому нужно сохранить файл.

    Асинхронно сохраняет файл в файловой системе.
    """
    # Получаем соответствующий механизм сохранения файла через фабрику
    file_saver = FileSaverFactory.get_saver(file, file_path)

    # Асинхронно сохраняем файл
    await file_saver.save_file()
