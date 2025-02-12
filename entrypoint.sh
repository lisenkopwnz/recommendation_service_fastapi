#!/bin/bash

set -e  # Останавливаем выполнение при ошибке

echo "Ожидание запуска PostgreSQL на $POSTGRES_HOST:$POSTGRES_PORT..."
timeout=120  # Время ожидания в секундах

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
    timeout=$((timeout - 1))
    if [ $timeout -le 0 ]; then
      echo "Ошибка: PostgreSQL не запустился за отведенное время."
      exit 1
    fi
done
echo "PostgreSQL запущен."

# Применяем миграции
echo "Применение миграций..."
alembic upgrade head || { echo "Ошибка: не удалось применить миграции"; exit 1; }
echo "Миграции успешно применены."

# Запуск FastAPI (без Celery)
echo "Запуск FastAPI..."
exec "$@"