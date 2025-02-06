from typing import Dict, Any, List, Generator
import pandas
from sqlalchemy import text
from sqlalchemy.orm import Session

from recommendation.storage.db.repository import DatabaseRepository


class SQLAlchemyRepository(DatabaseRepository):
    """
    Реализация репозитория для работы с базой данных через SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Инициализирует репозиторий.

        Args:
            session (Session): Сессия SQLAlchemy.
        """
        self.session = session

    def bulk_update(self, query: str, params: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """
        Выполняет массовое обновление данных.

        Args:
            query (str): SQL-запрос.
            params (List[Dict[str, Any]]): Список данных для массового обновления.

        Returns:
            Dict[str, Any] | None: Результат операции или None в случае успеха.
        """
        try:
            with self.session.begin():
                values = [{"id": item["id"], "recommended_ids": item["recommended_ids"]} for item in params]
                self.session.execute(text(query), values)
            return None  # Успешное выполнение
        except Exception as e:
            self.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def batch_generator(df: pandas.DataFrame, batch_size: int = 1000) -> Generator[List[Dict[str, Any]], None, None]:
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
