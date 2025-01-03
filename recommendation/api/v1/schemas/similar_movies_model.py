
class SimilarRecommendation(BaseModel):
    slug: str
    title: str
    description: str
    pub_date_time: datetime
    rating: float
    categories_content: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)