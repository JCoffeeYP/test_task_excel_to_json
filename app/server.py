import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import api_router

logging.basicConfig(
    format="%(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__file__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
