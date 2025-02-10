from sqlalchemy.ext.asyncio import AsyncSession

from recommendation.api.v1.adapters.models import engine


async def get_db():
    # Создаем сессию вручную через AsyncSession
    async with AsyncSession(engine) as session:
        yield session  # Генератор передает сессию для использования