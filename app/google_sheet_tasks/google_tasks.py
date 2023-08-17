import asyncio

from ..tasks.tasks import sync_db
from ..tasks.xlsx_parser import absolute_path
from .celery import celery_app
from .google import create_excel_from_google_sheets


@celery_app.task(name='update_db_from_google')
def update_tables_task_from_google_sheets():
    create_excel_from_google_sheets(absolute_path)
    return asyncio.run(sync_db())
