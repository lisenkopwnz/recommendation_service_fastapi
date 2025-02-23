from typing import Dict, Any, List, Generator
import pandas
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from recommendation.api.v1.domain.database_repository import DatabaseRepository


class SQLAlchemyRepository(DatabaseRepository):
    """
    Реализация репозитория для работы с базой данных через SQLAlchemy (асинхронно).
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализирует репозиторий.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session = session

    async def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): SQL-запрос.
            params (List[Dict[str, Any]]): Список данных для массового обновления.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        try:
            values = [{"id": item["id"], "recommended_ids": item["recommended_ids"]} for item in params]
            await self.session.execute(text(query), values)
        except Exception:
            raise

    async def get(self,model: Any, primary_key: int):
        """Находит запись по первичному ключу"""
        return await self.session.get(model, primary_key)

    async def commit(self):
        """
        Фиксирует транзакцию в базе данных.
        """
        await self.session.commit()

    async def rollback(self):
        """
        Откатывает транзакцию в базе данных.
        """
        await self.session.rollback()

    async def close(self):
        """
        Закрываем асинхронную сессию
        """
        await self.session.close()


    def batch_generator(self,df: pandas.DataFrame, batch_size: int = 1000) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Генератор, который возвращает данные из DataFrame пакетами.

        Args:
            df (pd.DataFrame): Входной DataFrame.
            batch_size (int): Размер пакета.

        Yields:
            List[Dict[str, Any]]: Пакет данных.
        """
        batch = []
        for _, row in df.iterrows():
            batch.append(row.to_dict())
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
