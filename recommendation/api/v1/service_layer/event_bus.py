import asyncio
from typing import Callable


class EventBus:
    """
    Шина событий, которая управляет подписчиками и уведомляет их о событиях.

    Методы:
    - subscribe(event_name: str, func: Callable): Подписывает обработчик на событие.
    - notify(event_name: str, *args, **kwargs): Уведомляет всех подписчиков о событии.
    """

    def __init__(self):
        """
        Инициализирует экземпляр EventBus с пустым словарём подписчиков.
        """
        self.subscribers = {}

    def subscribe(self, event_name: str, func: Callable):
        """
        Подписывает обработчик (функцию) на событие.

        :param event_name: Имя события, на которое подписывается обработчик.
        :param func: Функция-обработчик события.
        """
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(func)

    async def notify(self, event_name: str, *args, **kwargs):
        """
        Уведомляет всех подписчиков о наступлении события.

        :param event_name: Имя события, которое произошло.
        :param args: Аргументы, передаваемые подписчикам.
        :param kwargs: Ключевые аргументы, передаваемые подписчикам.
        """
        if event_name in self.subscribers:
            args = args or ()
            kwargs = kwargs or {}
            tasks = [subscriber(*args, **kwargs) for subscriber in self.subscribers[event_name]]
            await asyncio.gather(*tasks)
