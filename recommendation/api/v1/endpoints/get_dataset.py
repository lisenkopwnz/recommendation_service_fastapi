from fastapi import UploadFile, File, APIRouter, Request


from recommendation.api.v1.utils.data_sources.factory_saver import FileSaverFactory
from recommendation.config import settings

router = APIRouter(prefix="/api/v1/upload_file")

@router.post("/upload_dataset/")
async def upload_dataset(request: Request,file: UploadFile = File(...)):
    """
    Функция представления которая получает данные ,которые
    будут в дальнейшем использованы в построении рекомендаций
    """
    file_saver = FileSaverFactory.get_saver(file,settings.file_system_path)
    await file_saver.save_file()
    await request.app.state.event_bus.notify("generate_recommendations")
