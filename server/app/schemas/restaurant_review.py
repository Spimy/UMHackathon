from pydantic import BaseModel

class RestaurantReviewBase(BaseModel):
    restaurant: str
    rating: int
    review: str

class RestaurantReviewCreate(RestaurantReviewBase):
    pass

class RestaurantReview(RestaurantReviewBase):
    id: int

    class Config:
        orm_mode = True
