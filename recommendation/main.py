import uuid
from tkinter.font import names

from fastapi import FastAPI, Body
from starlette import status
from starlette.responses import FileResponse, JSONResponse

from recommendation.logging_config import setup_logger

setup_logger()

app = FastAPI()



@app.get("/")
def root(response):  # FastAPI передаст объект Response сюда
    # Устанавливаем заголовок в ответ
    response.headers["X-Custom-Header"] = "CustomValue"
    # Возвращаем тело ответа в формате JSON
    return {"message": "Hello, world!"}