import random

from .celery import celery_app

# from datetime import timedelta

# from celery import Celery, shared_task


@celery_app.task
def hello_world():
    i = random.randint(10, 30)
    print('Hello World!')

    with open(f'new_file{i}.txt', 'w') as fire:
        fire.write('Nonething')
