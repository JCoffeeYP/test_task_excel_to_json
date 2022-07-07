import os
from pathlib import Path

from celery import Celery

from service import convert_excel_file_to_json

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="handle_upload_file")
def handle_upload_file(path: str) -> None:
    try:
        convert_excel_file_to_json(Path(path))
    finally:
        Path(path).unlink()
