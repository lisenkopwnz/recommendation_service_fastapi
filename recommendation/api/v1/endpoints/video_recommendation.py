from fastapi import APIRouter, Query, HTTPException

from recommendation.api.v1.adapters.models import RecommendationResponse
from recommendation.api.v1.service_layer.similar_videos import get_similar_videos
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse

# Создаём роутер с префиксом "/api/v1/recommendation"
router = APIRouter(prefix="/api/v1/recommendation")


@router.get("/get_recommendation/")
async def get_recommendation(video_id: int = Query(..., ge=0)):
    """
    Получает список рекомендаций для видео на основе переданного video_id.

    Этот эндпоинт обращается к сервисному слою, который выполняет поиск похожих видео.
    Если рекомендации найдены, они возвращаются. Если подходящих видео нет,
    возвращается ошибка 404.

    Параметры:
    - **video_id** (int, query-параметр): ID видео, для которого запрашиваются рекомендации.
      Должен быть целым числом и не может быть отрицательным (ge=0).

    Возвращает:
    - **200 OK**: JSON с рекомендациями вида `{"data_recommendations": [...]}`.
    - **404 Not Found**: Если рекомендации не найдены.
    - **500 Internal Server Error**: В случае неожиданных ошибок сервера.
    """
    try:
        # Запрашиваем похожие видео через сервисный слой
        recommendations = await get_similar_videos(video_id)

        # Если рекомендации отсутствуют, выбрасываем HTTP-исключение с кодом 404
        if not recommendations:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Похожие видео не найдены."
            )

        # Возвращаем список рекомендованных видео с кодом 200
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "data_recommendations": RecommendationResponse(
                    id=video_id,
                    recommendation_id=recommendations).model_dump()
            }
        )

    except Exception as e:
        # Логируем и выбрасываем ошибку сервера с описанием проблемы
        raise Exception(f"Внутренняя ошибка сервера: {str(e)}")
