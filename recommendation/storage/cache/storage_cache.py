from typing import Any

import redis

from recommendation.storage.cache.cashe_repository import StorageRepository


class RedisStorage(StorageRepository):
    """ Низкоуровневый класс который реаизует кеширование с помошью Redis"""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        :param host: Имя хоста на котором будет работать redis сервер
        :param port: Номер порта на котором будет работать redis сервер
        :param db: Номер базы данных в деопазоне от 0 до 15(вкл)
        """
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self,key: str, value: Any):
        """ Метод для сохранения строкового значения по ключу"""
        self.client.set(f'{key}',f'{value}')
