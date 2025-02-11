from contextlib import asynccontextmanager

from fastapi import FastAPI

from recommendation.api.v1.task.worker import make_celery

app = FastAPI()

celery = make_celery()

@asynccontextmanager
async def lifespan():
    """
    Асинхронный контекстный менеджер для управления жизненным циклом приложения.

    Этот менеджер выполняет код при запуске и остановке приложения FastAPI.
    Используется для управления ресурсами, такими как соединения с базой данных.

    После завершения работы приложения (после `yield`), выполняется код для освобождения ресурсов.
    """
    yield
    engine.dispose()
