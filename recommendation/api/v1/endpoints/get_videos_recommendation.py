from fastapi import APIRouter, Query, HTTPException
from recommendation.api.v1.service_layer.get_recommendation import get_similar_videos
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.responses import JSONResponse

router = APIRouter(prefix="/api/v1/recommendation")


@router.get("/get_recommendation/")
async def get_recommendation(id: int = Query(..., ge=0)):
    """
    Эндпоинт для получения рекомендаций по видео на основе переданного ID.

    Этот эндпоинт возвращает список видео, похожих на видео с указанным ID.
    Для получения рекомендаций вызывается сервисный слой, который обрабатывает запрос
    и возвращает рекомендации в соответствующем формате.

    Аргументы:
        id (int): ID видео, по которому требуется получить рекомендации.
                  Должен быть целым числом и больше или равно 0 (ge=0).

    Возвращает:
        JSON: Список рекомендованных видео, похожих на указанное.
    """
    try:
        # Получаем похожие видео через сервисный слой
        recommendations = await get_similar_videos(id)

        # Если рекомендаций нет, выбрасываем 404
        if not recommendations:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Похожие видео не найдены."
            )

        # Возвращаем успешный ответ с кодом 200 и рекомендациями
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={
                "data": recommendations
            }
        )

    except HTTPException as e:
        # Если ошибка HTTP (например, 404), выбрасываем её с данными
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        # В случае ошибки сервера (500) возвращаем внутреннюю ошибку
        raise Exception(f"Внутренняя ошибка сервера: {str(e)}")
    