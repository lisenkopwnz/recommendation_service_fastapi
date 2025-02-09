import json
from typing import Any, List, Dict

import redis

from recommendation.api.v1.domain.cashe_repository import StorageRepository

class RedisStorage(StorageRepository):
    """ Низкоуровневый класс, который реализует кеширование с помощью Redis """

    def __init__(self, host: str = 'localhost', port: int = 6379, new_db: int = 0, old_db: int = 1):
        """
        :param host: Имя хоста на котором будет работать redis сервер
        :param port: Номер порта на котором будет работать redis сервер
        :param db: Номер базы данных в диапазоне от 0 до 15 (включительно)
        """
        self.new_client = redis.Redis(host=host, port=port, db=new_db)
        self.old_client = redis.Redis(host=host, port=port, db=old_db)

    def bulk_set(self, data: List[Dict[str, Any]]):
        """Метод для массового сохранения данных в Redis."""
        with self.new_client.pipeline() as pipe_new, self.old_client.pipeline() as pipe_old:
            for item in data:
                key = f'videos_id:{str(item["id"])}'
                value = json.dumps(item["recommended_ids"])

                old_value = self.new_client.get(key)
                if old_value:
                   pipe_old.set(key, old_value)

                pipe_new.set(key, value)
                pipe_new.execute()
                pipe_old.execute()

    def get(self, key: str):
        """ Получаем значение по ключу """
        return self.new_client.get(f'videos_id:{key}')

    def commit(self):
        """ Подтверждаем изменения, очищая всё старое хранилище Redis. """
        self.old_client.flushdb()

    def rollback(self):
        """ Откатываем изменения, восстанавливая данные из старого хранилища. """
        with self.new_client.pipeline() as pipe_new, self.old_client.pipeline() as pipe_old:
            for key in self.old_client.keys():  # Получаем все ключи из старого хранилища
                old_value = self.old_client.get(key)
                if old_value:
                    pipe_new.set(key, old_value)  # Восстанавливаем старые данные
                pipe_old.delete(key)  # Удаляем восстановленные данные

            # Выполняем откат
            pipe_new.execute()
            pipe_old.execute()
