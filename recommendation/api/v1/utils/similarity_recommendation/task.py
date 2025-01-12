from sqlalchemy.orm import Session

from recommendation.api.v1.utils.similarity_recommendation.recommendation_engine import RecommendationEnginePandas
from recommendation.api.v1.utils.similarity_recommendation.recommendation_service import RecommendationService
from recommendation.config import settings
from recommendation.db.models import SessionLocal


@shared_task
def generate_recommendation_task():
    db: Session = SessionLocal()
    try:
        # Создаём движок
        engine = RecommendationEnginePandas(settings.file_system_path,20)

        # Создаём сервис и передаём ему движок
        service = RecommendationService(engine)

        result = service.generate_recommendations()

        return result
    except:
        pass
    finally:
        # Закрываем
        db.close()
