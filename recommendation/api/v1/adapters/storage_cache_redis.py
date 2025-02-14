import json
from typing import Any, List, Dict

import redis.asyncio as redis

from recommendation.api.v1.domain.cashe_repository import StorageRepository

class AsyncRedisStorage(StorageRepository):
    """Низкоуровневый класс, который реализует кеширование с помощью Redis в асинхронном режиме"""

    def __init__(self, host: str = '172.17.0.1', port: int = 6379, new_db: int = 0, old_db: int = 1):
        """
        :param host: Имя хоста на котором будет работать redis сервер
        :param port: Номер порта на котором будет работать redis сервер
        :param db: Номер базы данных в диапазоне от 0 до 15 (включительно)
        """
        self.host = host
        self.port = port
        self.new_db = new_db
        self.old_db = old_db

    async def _get_client(self, db: int):
        # Новый способ создания подключения через Redis класс
        redis_client = redis.Redis.from_url(f"redis://{self.host}:{self.port}/{db}", encoding="utf-8", decode_responses=True,max_connections=100)
        return redis_client

    async def bulk_set(self, data: List[Dict[str, Any]]):
        """Метод для массового сохранения данных в Redis."""
        new_client = await self._get_client(self.new_db)
        old_client = await self._get_client(self.old_db)

        async with new_client.pipeline() as pipe_new, old_client.pipeline() as pipe_old:
            for item in data:
                key = f'videos_id:{str(item["id"])}'
                value = json.dumps(item["recommended_ids"])

                old_value = await new_client.get(key)
                if old_value:
                    await pipe_old.set(key, old_value)

                await pipe_new.set(key, value)

            await pipe_new.execute()
            await pipe_old.execute()

    async def get(self, key: str):
        """Получаем значение по ключу"""
        new_client = await self._get_client(self.new_db)
        value = await new_client.get(f'videos_id:{key}')
        return value

    async def commit(self):
        """Подтверждаем изменения, очищая всё старое хранилище Redis."""
        old_client = await self._get_client(self.old_db)
        await old_client.flushdb()

    async def rollback(self):
        """Откатываем изменения, восстанавливая данные из старого хранилища."""
        new_client = await self._get_client(self.new_db)
        old_client = await self._get_client(self.old_db)

        async with new_client.pipeline() as pipe_new, old_client.pipeline() as pipe_old:
            keys = await old_client.keys()
            for key in keys:
                old_value = await old_client.get(key)
                if old_value:
                    await pipe_new.set(key, old_value)  # Восстанавливаем старые данные
                await pipe_old.delete(key)  # Удаляем восстановленные данные

            await pipe_new.execute()
            await pipe_old.execute()

    async def close(self):
        """ Метод не реализовывает логики так как пул соеденений Redis автомвтически закрывает соедения"""
        pass
