from celery import Celery

# from .celery_config import celery_setting
from ..config import settings

celery_app = Celery(broker=f'amqp://guest:guest@{settings.rabbit_host}:{settings.rabbit_port}')
# celery_app.config_from_object(celery_setting)
celery_app.conf.beat_schedule = {
        'create_file': {
            'task': 'hello',
            'schedule': 5,
            # 'args': (None,),
        },
    }

celery_app.conf.broker_connection_retry_on_startup = True