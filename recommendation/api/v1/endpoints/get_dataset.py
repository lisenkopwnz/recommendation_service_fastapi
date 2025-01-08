from fastapi import UploadFile, File

from recommendation.api.v1.utils.data_sources.factory_saver import FileSaverFactory
from recommendation.main import app
from recommendation.config import settings

@app.post("/get_recommendation_dataset/")
async def get_recommendation_dataset(file: UploadFile = File(...)):
    """
    Функция представления которая получает данные ,которые
    будут в дальнейшем использованы в построении рекомендаций
    """
    file_saver = FileSaverFactory.get_saver(file,settings.file_system_path)
    await file_saver.save_file()
