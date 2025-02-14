from contextlib import asynccontextmanager

from fastapi import FastAPI

from recommendation.api.v1.endpoints.get_dataset import router as file_router
from recommendation.api.v1.endpoints.get_similar_videos_recommendation import router as recommendation_router
from recommendation.api.v1.service_layer.event_bus import EventBus
from recommendation.api.v1.service_layer.event_handlers import generate_recommendations_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекстный менеджер для управления жизненным циклом приложения.
    """
    # Код, выполняемый при запуске приложения
    app.state.event_bus = EventBus()
    app.state.event_bus.subscribe("generate_recommendations", generate_recommendations_handler)

    yield
    # Код, выполняемый при остановке приложения
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(recommendation_router)
app.include_router(file_router)