from typing import Dict, Any

from sqlalchemy.orm import Session

from recommendation.db.repository import DatabaseRepository


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

    def bulk_update(self, query: str, params: Dict[str, Any]) -> None:
        pass