from sqlmodel import SQLModel, Field
from typing import Optional

class RestaurantReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant: int
    rating: int
    review: str
