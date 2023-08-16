from celery import Celery

# from .celery_config import celery_setting
from ..config import settings

# celery_app.config_from_object(celery_setting)
celery_app = Celery(broker=f'amqp://guest:guest@{settings.rabbit_host}:{settings.rabbit_port}')
celery_app.conf.beat_schedule = {
    'update_db': {
        'task': 'update_db',
        'schedule': 15,
    },
    # 'create_db': {
    # 'task': 'create_db',
    # 'schedule': 14,
    # },
}

celery_app.conf.broker_connection_retry_on_startup = True
