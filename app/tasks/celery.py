from celery import Celery

from ..config import settings

celery_app = Celery(broker=f'amqp://guest:guest@{settings.rabbit_host}:{settings.rabbit_port}')
celery_app.conf.beat_schedule = {
    'update_db': {
        'task': 'update_db',
        'schedule': 15,
    },
}

celery_app.conf.broker_connection_retry_on_startup = True
