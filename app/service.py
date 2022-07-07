import json
import shutil
from datetime import datetime, time
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Optional

from fastapi import UploadFile
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def data_type_definition(value: Any):

    if isinstance(value, datetime) or isinstance(value, time):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    elif isinstance(value, str):
        try:
            formatted_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            return formatted_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        except ValueError:
            pass
        try:
            formatted_value = json.loads(value)
            for key, obj in formatted_value.items():
                formatted_value[key] = data_type_definition(obj)
            return formatted_value
        except (TypeError, AttributeError, json.decoder.JSONDecodeError):
            pass
    elif isinstance(value, dict):
        for key, obj in value.items():
            value[key] = data_type_definition(obj)
    return value


def check_empty_row(row: dict) -> bool:
    """
    Данная проверка нужна для того, чтобы не учитывать пустые строки в конце файла
    """
    empty_cell_count = 0
    for value in row.values():
        if not value:
            empty_cell_count += 1
    if empty_cell_count == len(row):
        return True
    return False


def parse_excel_file(filename: Path) -> dict:
    wb = load_workbook(filename=filename)

    result: dict = {}

    for sheet in wb:
        result[sheet.title]: list = []
        wb.active = sheet
        ws: Worksheet = wb.active
        last_column: int = len(list(ws.columns))
        last_row: int = len(list(ws.rows))

        for row in range(1, last_row + 1):
            row_value: dict = {}
            for column in range(1, last_column + 1):
                column_letter: str = get_column_letter(column)
                intermediate_value: Any = ws[f"{column_letter}{row}"].value
                if row > 1 and ws[f"{column_letter}1"].value is not None:
                    row_value[ws[f"{column_letter}1"].value] = data_type_definition(
                        intermediate_value
                    )
            if row_value and not check_empty_row(row_value):
                result[sheet.title].append(row_value)
    wb.close()
    return result


def convert_excel_file_to_json(tmp_filename: Path, json_filename: Path) -> None:
    parsed_excel: dict = parse_excel_file(tmp_filename)
    data: str = json.dumps(parsed_excel, indent=4, ensure_ascii=False)
    with open(f"{tmp_filename.with_suffix('.json')}", "w", encoding="utf-8") as f:
        f.write(data)


def check_existing_files(upload_file: UploadFile):

    current_directory = Path("../json_output_data")
    json_filename: Path = current_directory.joinpath(
        Path(upload_file.filename).with_suffix(".json")
    )

    for file in current_directory.iterdir():
        if file == json_filename:
            return False
    return True
