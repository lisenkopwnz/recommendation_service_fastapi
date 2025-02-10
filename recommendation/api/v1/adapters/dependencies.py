from sqlalchemy.ext.asyncio import AsyncSession

from recommendation.api.v1.adapters.models import engine


async def get_db():
    """Создает и возвращает сессию."""
    session = AsyncSession(engine)
    return session
