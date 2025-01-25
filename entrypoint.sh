#!/bin/bash

# Ожидание запуска PostgreSQL
echo "Ожидание запуска PostgreSQL на $POSTGRES_HOST:$POSTGRES_PORT..."
timeout=240

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
      echo "Ошибка: PostgreSQL не запустился за отведённое время."
      exit 1
    fi
done

echo "PostgreSQL запущен. Начинаем подготовку приложения..."

# Применение миграций, если они есть
echo "Применение миграций..."

# Создание миграций (если нужно)
if ! alembic revision --autogenerate -m "Auto-generated migration"; then
    echo "Ошибка: не удалось создать миграции"
    exit 1
fi

# Применение миграций
if ! alembic upgrade head; then
    echo "Ошибка: не удалось применить миграции"
    exit 1
fi

echo "Миграции успешно применены."

# Запуск основного приложения FastAPI
exec "$@"
