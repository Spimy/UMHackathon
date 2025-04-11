from pydantic import BaseModel


class ReviewBase(BaseModel):
    merchant_id: str
    rating: int
    review: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
