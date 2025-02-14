import json
from typing import Any, List, Dict

import redis.asyncio as redis

from recommendation.api.v1.domain.cashe_repository import StorageRepository


class AsyncRedisStorage(StorageRepository):
    """Асинхронное кеш-хранилище Redis, использующее базу 1 только при обновлении данных."""

    def __init__(self, host: str = "172.17.0.1", port: int = 6379, new_db: int = 0, old_db: int = 1, max_connections: int = 100):
        """
        :param host: Хост Redis
        :param port: Порт Redis
        :param new_db: База данных для работы (основная)
        :param old_db: Временная база данных (используется только при обновлении)
        :param max_connections: Максимальное количество соединений
        """
        self.host = host
        self.port = port
        self.new_db = new_db
        self.old_db = old_db

        # Пул соединений только для базы 0 (основной)
        self.new_pool = redis.ConnectionPool(
            host=host, port=port, db=new_db, max_connections=max_connections, encoding="utf-8", decode_responses=True
        )
        self.new_client = redis.Redis(connection_pool=self.new_pool)

        # Старый клиент создаем как None, чтобы открывать только при необходимости
        self.old_client = None

    async def _get_old_client(self):
        """Создает клиент Redis для базы 1 (если еще не создан)."""
        if self.old_client is None:
            self.old_client = redis.Redis(
                host=self.host, port=self.port, db=self.old_db, encoding="utf-8", decode_responses=True
            )
        return self.old_client

    async def bulk_set(self, data: List[Dict[str, Any]]):
        """Обновляет данные в Redis, сохраняя предыдущие значения в базе 1."""
        old_client = await self._get_old_client()

        async with self.new_client.pipeline() as pipe_new, old_client.pipeline() as pipe_old:
            for item in data:
                key = f'videos_id:{item["id"]}'
                value = json.dumps(item["recommended_ids"])

                # Копируем старое значение в old_db перед обновлением
                old_value = await self.new_client.get(key)
                if old_value:
                    await pipe_old.set(key, old_value)

                # Записываем новое значение в new_db
                await pipe_new.set(key, value)

            await pipe_new.execute()
            await pipe_old.execute()

    async def get(self, key: str) -> Any:
        """Получаем значение из базы 0."""
        return await self.new_client.get(f'videos_id:{key}')

    async def commit(self):
        """Удаляет данные из базы 1 (подтверждает изменения в базе 0)."""
        if self.old_client:
            await self.old_client.flushdb()

    async def rollback(self):
        """Откатывает обновление, восстанавливая старые данные из базы 1."""
        if not self.old_client:
            return  # Если old_client не создавался, откатывать нечего

        async with self.new_client.pipeline() as pipe_new, self.old_client.pipeline() as pipe_old:
            keys = await self.old_client.keys()
            for key in keys:
                old_value = await self.old_client.get(key)
                if old_value:
                    await pipe_new.set(key, old_value)  # Восстанавливаем старые данные
                await pipe_old.delete(key)  # Удаляем восстановленные данные

            await pipe_new.execute()
            await pipe_old.execute()

    async def close(self):
        """Закрывает соединения с Redis."""
        await self.new_client.aclose()
        if self.old_client:
            await self.old_client.aclose()  # Закрываем только если old_client был создан
