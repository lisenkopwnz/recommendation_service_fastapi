from contextlib import asynccontextmanager

from fastapi import FastAPI

from recommendation.api.v1.endpoints.get_dataset import router as file_router
from recommendation.api.v1.endpoints.get_similar_videos_recommendation import router as recommendation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекстный менеджер для управления жизненным циклом приложения.
    """
    # Код, выполняемый при запуске приложения
    print("Starting up...")
    yield
    # Код, выполняемый при остановке приложения
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(recommendation_router)
app.include_router(file_router)