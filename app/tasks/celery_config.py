from datetime import timedelta


# todo добавить в .env файл rabbitmq
class Config:
    broker_connection_retry_on_startup = True
    broker_url = 'amqp://guest:guest@rabbitmq:5672//'
    result_backend = 'rpc://'
    result_persistent = False
    timezone = 'Europe/Moscow'
    beat_schedule = {
        'every_15_sconds': {
            'tasks': 'app.tasks.tasks.hello_world',
            'schedule': timedelta(seconds=15),
        }
    }


celery_setting = Config()
