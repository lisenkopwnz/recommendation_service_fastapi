from fastapi import APIRouter, Query
from recommendation.api.v1.service_layer.get_similar_recommendation import get_similar_videos

router = APIRouter(prefix="/api/v1/recommendation")

@router.get("/get_recommendation/")
async def get_recommendation(id: int = Query(..., ge=0)):
    return await get_similar_videos(id)