from http import HTTPStatus
from fastapi import UploadFile, File, APIRouter, Request, HTTPException
from starlette.responses import JSONResponse
from recommendation.config import settings

# Создаем новый роутер с префиксом "/api/v1/file"
router = APIRouter(prefix="/api/v1/file")


@router.post("/upload_dataset/")
async def upload_dataset(request: Request, file: UploadFile = File(...)):
    """
    Эндпоинт для загрузки датасета и инициирования процесса генерации рекомендаций.

    1. Загружает файл и уведомляет шину событий о загрузке.
    2. Инициирует генерацию рекомендаций через событие.

    Параметры:
        request (Request): Объект запроса, используется для получения доступа к шине событий.
        file (UploadFile): Загружаемый файл, который будет использован для генерации рекомендаций.

    Возвращает:
        JSONResponse: Ответ с сообщением о статусе выполнения.
    """
    try:
        # Уведомляем шину событий о загрузке файла, передавая файл и путь для сохранения
        await request.app.state.event_bus.notify(
            "file_uploaded", file=file, file_path=settings.file_system_path
        )

        # Инициируем процесс генерации рекомендаций
        await request.app.state.event_bus.notify("generate_recommendations")

        # Возвращаем успешный ответ с кодом 200 и сообщением о запуске процесса рекомендаций
        return JSONResponse(
            status_code=HTTPStatus.OK,  # Код 200: ОК
            content={"message": "Набор данных успешно загружен. Начата генерация рекомендаций."}
        )

    except Exception as e:
        # В случае ошибки возвращаем код 500 и сообщение об ошибке
        raise Exception(f"Внутренняя ошибка сервера: {str(e)}")

    except HTTPException as e:
        # Обрабатываем исключения HTTP и повторно выбрасываем их
        raise HTTPException(status_code=e.status_code, detail=e.detail)
