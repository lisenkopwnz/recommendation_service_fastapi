import asyncio

from recommendation.config import settings
import aiofiles

class DataLoader:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    async def load_data(self):
        """Загружает CSV-файл в DataFrame."""
        df = await asyncio.to_thread(
            spark.read.csv, self.save_path, header=True, inferSchema=True
        )

        # Проверяем наличие необходимых колонок
        required_columns = ["movie_id", "title", "description", "rating", "publication_date", "categories", "tags"]
        if not all(column in df.columns for column in required_columns):
            raise ValueError(
                "CSV должен содержать колонки: movie_id, title, description, rating, publication_date, categories, tags")

        return df