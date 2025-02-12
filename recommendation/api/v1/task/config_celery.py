import os


class Config:
    CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"
    CELERY_RESULT_BACKEND = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/2"
    CELERY_TIMEZONE = 'UTC'
    CELERY_TASK_TIME_LIMIT = 86400
    CELERY_TASK_DEFAULT_RETRY_DELAY = 60
    CELERY_TASK_MAX_RETRIES = 3