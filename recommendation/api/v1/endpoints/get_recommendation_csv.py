from fastapi import UploadFile, File

from recommendation.main import app


@app.post("/get_recommendation_dataset/")
def get_recommendation_dataset(file: UploadFile = File(...)):
    """
    Функция представления которая получает данные ,которые
    будут в дальнейшем использованы в построении рекомендаций
    """
    pass