# Оф. образ Python
FROM python:3.12-slim-bullseye

# Переменные окружения для Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Установка рабочей директории
WORKDIR /recommendation_system

# Настройка временной зоны UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

# Системные зависимости (для сборки и PostgreSQL клиента)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копирую файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Все файлы проекта копируются в контейнер
COPY . .

# Исполняемый скрипт entrypoint.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Порт для FastAPI
EXPOSE 8000

# Устанавливаю entrypoint для запуска сервера uvicorn
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Команда для запуска uvicorn-сервера
CMD ["uvicorn", "recommendation.main:app", "--host", "0.0.0.0", "--port", "8000"]
