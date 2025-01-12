from contextlib import asynccontextmanager

from fastapi import FastAPI

from recommendation.db.models import engine

app = FastAPI()

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
