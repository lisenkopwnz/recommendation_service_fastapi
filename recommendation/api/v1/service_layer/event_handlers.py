from recommendation.api.v1.service_layer.task import generate_recommendation_task

async def generate_recommendations_handler():
    generate_recommendation_task.delay()