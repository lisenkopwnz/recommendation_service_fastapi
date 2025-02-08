from fastapi import Query

from recommendation.main import app


@app.get("/get_recommendation/")
async def get_recommendation(id: int = Query(..., ge=0)):
    """ Эндпоинт для полученя списка рекомендаций из кеша(при наличии) или базы данных """
    pass