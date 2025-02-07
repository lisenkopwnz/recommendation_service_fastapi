import json
from typing import Any, List, Dict

import redis

from recommendation.storage.cache.cashe_repository import StorageRepository

class RedisStorage(StorageRepository):
    """ Низкоуровневый класс, который реализует кеширование с помощью Redis """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        :param host: Имя хоста на котором будет работать redis сервер
        :param port: Номер порта на котором будет работать redis сервер
        :param db: Номер базы данных в диапазоне от 0 до 15 (включительно)
        """
        self.client = redis.Redis(host=host, port=port, db=db)

    def bulk_set(self, data: List[Dict[str, Any]]):
        """Метод для массового сохранения данных в Redis."""
        with self.client.pipeline() as pipe:
            for item in data:
                key = str(item["id"])  # Делаем ключ строкой (Redis работает только с строковыми ключами)
                value = json.dumps(item["recommended_ids"])  # Сериализуем список в JSON
                pipe.set(key, value)
            pipe.execute()  # Выполняем все команды за один запрос
