from celery import Celery

from recommendation.api.v1.task.config_celery import Config


celery = Celery("celery_recommendation_app", broker=Config.CELERY_BROKER_URL)

celery.conf.update(
    result_backend=Config.CELERY_RESULT_BACKEND,
    timezone=Config.CELERY_TIMEZONE,
    task_default_retry_delay=Config.CELERY_TASK_DEFAULT_RETRY_DELAY,
    task_max_retries=Config.CELERY_TASK_MAX_RETRIES,
    task_time_limit=Config.CELERY_TASK_TIME_LIMIT
)
