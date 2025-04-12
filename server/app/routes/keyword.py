from fastapi import APIRouter
import crud
from schemas import Keyword, KeywordCreate
from models import SessionDep

router = APIRouter(tags=["keywords"])


@router.post("/keywords/", response_model=Keyword)
def create_keyword(keyword: KeywordCreate, session: SessionDep):
    return crud.create_keyword(session, keyword.dict())


@router.get("/keywords/", response_model=list[Keyword])
def read_keywords(session: SessionDep, skip: int = 0, limit: int = 10):
    keywords = crud.get_keywords(session, skip=skip, limit=limit)
    return [keyword[0] for keyword in keywords]


@router.get("/keywords/by-category/")
def read_keywords_by_category(session: SessionDep):
    return crud.get_keywords_by_category(session)
