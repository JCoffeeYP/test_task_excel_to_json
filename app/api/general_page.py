import logging
import os
from pathlib import Path
from typing import Union

from celery.result import AsyncResult
from fastapi import APIRouter, Request, UploadFile, status
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from service import check_existing_files, save_upload_file
from worker import handle_upload_file

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__file__)

general_page_router = APIRouter()


@general_page_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@general_page_router.post("/upload/excel")
def create_upload_excel_file(file: Union[UploadFile, None] = None):
    storage_dir = os.environ.get("STORAGE_DIR", "json_output_data")
    if not file:
        logger.info("Файл не был загружен")
        return JSONResponse(
            {"message": "Файл не был загружен"}, status_code=status.HTTP_204_NO_CONTENT
        )
    if not check_existing_files(file):
        logger.info("Файл уже существует")
        return JSONResponse(
            {"message": "Файл уже существует"}, status_code=status.HTTP_204_NO_CONTENT
        )
    tmp_file_path: Path = Path("../..", storage_dir, file.filename)
    save_upload_file(file, tmp_file_path)
    task = handle_upload_file.delay(str(tmp_file_path))
    return JSONResponse(
        {"message": "Обработка файла запущена", "task_id": task.id},
        status_code=status.HTTP_200_OK,
    )


@general_page_router.get("/upload/excel/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    return JSONResponse(result, status_code=status.HTTP_200_OK)
