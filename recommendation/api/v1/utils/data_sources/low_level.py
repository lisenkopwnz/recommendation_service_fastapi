from recommendation.config import settings


class FileHandler:
    def __init__(self, file, save_path = settings.file_system_path):
        self.file = file
        self.save_path = save_path

    async def save_file(self):
        # Сохраняем файл
        with open(self.save_path, "wb") as buffer:
            buffer.write(await self.file.read())
