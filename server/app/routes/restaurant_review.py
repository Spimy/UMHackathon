from fastapi import APIRouter
import crud
from schemas import RestaurantReview, RestaurantReviewCreate
from models import SessionDep

router = APIRouter(tags=["restaurant_reviews"])


@router.post("/reviews/", response_model=RestaurantReview)
def create_review(review: RestaurantReviewCreate, session: SessionDep):
    return crud.create_review(session, review.dict())


@router.get("/reviews/", response_model=list[RestaurantReview])
def read_reviews(session: SessionDep, skip: int = 0, limit: int = 10):
    reviews = crud.get_reviews(session, skip=skip, limit=limit)
    return [review[0] for review in reviews]
