from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from recommendation.api.v1.endpoints.get_dataset import router as file_router
from recommendation.api.v1.endpoints.get_videos_recommendation import router as recommendation_router
from recommendation.api.v1.service_layer.event_bus import EventBus
from recommendation.api.v1.service_layer.event_handlers import generate_recommendations_handler, save_file_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекстный менеджер для управления жизненным циклом приложения FastAPI.

    При старте приложения создается и настраивается шина событий. На шину подписываются обработчики событий,
    такие как обработка загрузки файла и генерация рекомендаций.

    Этот контекстный менеджер запускается при старте и завершении работы приложения, позволяя управлять
    ресурсами, связанными с жизненным циклом.

    Параметры:
        app (FastAPI): Объект приложения FastAPI.

    Рекомендуемая логика:
        1. Создать шину событий в `app.state`.
        2. Подписать обработчики на соответствующие события.
        3. После выполнения задач на выходе шина событий и подписчики очищаются.
    """
    # Создание и настройка шины событий
    app.state.event_bus = EventBus()
    # Подписка обработчиков на события
    app.state.event_bus.subscribe("generate_recommendations", generate_recommendations_handler)
    app.state.event_bus.subscribe("file_uploaded", save_file_handler)

    # Передаем управление приложению
    yield

    # Очистка при завершении работы приложения
    print("Shutting down...")


# Инициализация приложения FastAPI с управлением жизненным циклом через контекстный менеджер
app = FastAPI(lifespan=lifespan)

# Глобальный обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code = 400,
        content={"message": "Ошибка валидации данных", "errors": exc.errors()}
    )

# Глобальный обработчик HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "path": request.url.path}
    )

# Глобальный обработчик для всех остальных исключений (например, ValueError)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"Произошла непредвиденная ошибка": str(exc), "path": request.url.path}
    )

# Подключение маршрутов для обработки запросов на рекомендации и загрузку файлов
app.include_router(recommendation_router)
app.include_router(file_router)
