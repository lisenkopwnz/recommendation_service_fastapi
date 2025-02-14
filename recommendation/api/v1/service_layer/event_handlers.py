from recommendation.api.v1.service_layer.task import generate_recommendation_task
from recommendation.api.v1.utils.data_sources.factory_saver import FileSaverFactory


async def generate_recommendations_handler():
    generate_recommendation_task.delay()

async def save_file_handler(file, file_path):
    file_saver = FileSaverFactory.get_saver(file, file_path)
    await file_saver.save_file()