import os
import time
from pathlib import Path

from celery import Celery
from fastapi import UploadFile

from service import save_upload_file_tmp, convert_excel_file_to_json

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


# @celery.task(name="handle_upload_file")
# def handle_upload_file(path: str) -> None:
#     # upload_file: UploadFile = None
#     json_filename: Path = Path(upload_file.filename).with_suffix(".json")
#     tmp_path: Path = save_upload_file_tmp(upload_file)
#
#     try:
#         convert_excel_file_to_json(tmp_path, json_filename)
#     finally:
#         tmp_path.unlink()


@celery.task(name="handle_upload_file")
def handle_upload_file(path: str) -> None:
    json_filename: Path = Path(path).with_suffix(".json")

    try:
        convert_excel_file_to_json(Path(path), json_filename)
    finally:
        Path(path).unlink()

