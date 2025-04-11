from sqlmodel import SQLModel, Field
from typing import Optional


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    merchant_id: str
    rating: int
    review: str
