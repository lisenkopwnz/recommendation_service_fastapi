from recommendation.api.v1.schemas.similar_movies_model import SimilarRecommendation
from recommendation.main import app


@app.post("/recommendations/similar/")
def recommendations_similar(data: SimilarRecommendation):
    pass
