from celery import Celery

from .celery_config import celery_setting

celery_app = Celery('tasks')
celery_app.config_from_object(celery_setting)
