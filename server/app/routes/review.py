from fastapi import APIRouter
import crud
from schemas import Review, ReviewCreate
from models import SessionDep

router = APIRouter(tags=["reviews"])


@router.post("/reviews/", response_model=Review)
def create_review(review: ReviewCreate, session: SessionDep):
    return crud.create_review(session, review.dict())

@router.get("/reviews/", response_model=list[Review])
def read_reviews(session: SessionDep, skip: int = 0, limit: int = 10):
    reviews = crud.get_reviews(session, skip=skip, limit=limit)
    return [review[0] for review in reviews]

@router.get("/reviews/{merchant_id}", response_model=list[Review])
def get_reviews_by_merchant_id(merchant_id: str, session: SessionDep):
    reviews = crud.get_reviews_by_merchant(session, merchant_id)
    return [review for review in reviews]