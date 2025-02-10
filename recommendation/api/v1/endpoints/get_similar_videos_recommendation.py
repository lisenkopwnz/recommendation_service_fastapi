import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

from fastapi import Query

from recommendation.api.v1.service_layer.get_similar_recommendation import get_similar_videos
from recommendation.main import app


@app.get("/get_recommendation/")
async def get_recommendation(id: int = Query(..., ge=0)):
    """ Эндпоинт для получения списка рекомендаций из кэша (при наличии) или базы данных """

