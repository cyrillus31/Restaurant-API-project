import random

from .celery import celery_app

# from datetime import timedelta

# from celery import Celery, shared_task


@celery_app.task(name='hello')
def hello_world():
    i = random.randint(100, 300)
    print('Hello World!')

    with open(f'zzzdelete_this{i}.txt', 'w') as fire:
        fire.write('Nonething')
