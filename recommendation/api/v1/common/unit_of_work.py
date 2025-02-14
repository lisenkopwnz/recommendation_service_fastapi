from recommendation.api.v1.adapters.storage_cache_redis import AsyncRedisStorage
from recommendation.api.v1.service_layer.manager_database import DataBaseService


class AsyncUnitOfWork:
    """
    Контекстный менеджер для работы с базой данных и кешем через высокоуровневые сервисы.

    Обеспечивает управление транзакциями: при успешном выполнении блока кода фиксирует (commit)
    изменения в базе данных и кеше, а при ошибке откатывает (rollback) их.

    Атрибуты:
        db_service: Объект сервиса работы с базой данных.
        cache_service: Объект сервиса работы с кешем.
    """

    def __init__(self, db_service: DataBaseService = None, cache_service: AsyncRedisStorage = None):
        """
        Инициализирует контекстный менеджер.

        Параметры:
            db_service: Экземпляр сервиса базы данных, управляющий транзакциями.
            cache_service: Экземпляр сервиса кеша, управляющий транзакциями.
        """
        self.db_service = db_service
        self.cache_service = cache_service

    async def __aenter__(self):
        """
        Вход в асинхронный контекстный менеджер.

        Возвращает:
            self: Объект UnionOfWork.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из асинхронного контекстного менеджера.

        Если в блоке контекста возникло исключение, выполняется откат (rollback)
        изменений в базе данных и кеше. В противном случае изменения фиксируются (commit).

        Параметры:
            exc_type: Тип исключения (если возникло).
            exc_val: Значение исключения (если возникло).
            exc_tb: Трассировка стека исключения (если возникло).
        """
        if exc_type:
            await self.rollback()
            await self.close()
        else:
            await self.commit()
            await self.close()

    async def commit(self):
        """
        Фиксирует изменения в базе данных и кеше.
        """
        if self.db_service:
            await self.db_service.commit()
        if self.cache_service:
            await self.cache_service.commit()

    async def rollback(self):
        """
        Откатывает изменения в базе данных и кеше.
        """
        if self.db_service:
            await self.db_service.rollback()
        if self.cache_service:
            await self.cache_service.rollback()

    async def close(self):
        """
        Закрывает соеденение в базе данных и кеше.
        """
        if self.db_service:
            await self.db_service.close()
        if self.cache_service:
            await self.cache_service.close()
