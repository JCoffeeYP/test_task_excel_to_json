from pathlib import Path
from typing import Union, Optional

from fastapi import FastAPI, UploadFile

from service import check_existing_files, save_upload_file, save_upload_file_tmp
from worker import handle_upload_file

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.post("/upload/excel")
# async def create_upload_excel_file(file: Union[UploadFile, None] = None):
#     if not file:
#         return {"message": "Файл не был загружен"}
#     if not check_existing_files(file):
#         return {"message": "Файл уже существует"}
#     save_upload_file(file, Path(f'./app/tmp/{file.filename}'))
#     handle_upload_file.delay(f'./app/tmp/{file.filename}')
#     return {"message": "Обработка файла запущена"}


@app.post("/upload/excel")
def create_upload_excel_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "Файл не был загружен"}
    if not check_existing_files(file):
        return {"message": "Файл уже существует"}
    tmp_file_path: Path = Path("..", "json_output_data", file.filename)
    save_upload_file(file, tmp_file_path)
    # tmp_file_path: Path = save_upload_file_tmp(file)
    handle_upload_file.delay(str(tmp_file_path))
    return {"message": "Обработка файла запущена"}
