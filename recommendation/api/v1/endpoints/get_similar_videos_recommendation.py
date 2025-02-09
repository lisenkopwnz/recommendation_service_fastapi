import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

from fastapi import Query

from recommendation.api.v1.service_layer.get_similar_recommendation import get_similar_videos
from recommendation.main import app

# Создаем пул потоков с ограничением на количество потоков
executor = ThreadPoolExecutor(max_workers=100)  # Максимум 100 потоков

@app.get("/get_recommendation/")
async def get_recommendation(id: int = Query(..., ge=0)):
    """ Эндпоинт для получения списка рекомендаций из кэша (при наличии) или базы данных """
    loop = asyncio.get_running_loop()

    # Используем пул потоков для выполнения синхронной функции
    return await loop.run_in_executor(executor, get_similar_videos, id)
