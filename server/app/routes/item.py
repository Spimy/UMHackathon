from fastapi import APIRouter
import crud
from schemas import Item, ItemCreate
from models import SessionDep

router = APIRouter(tags=["items"])


@router.post("/items/", response_model=Item)
def create_item(item: ItemCreate, session: SessionDep):
    return crud.create_item(session, item.dict())


@router.get("/items/", response_model=list[Item])
def read_items(session: SessionDep, skip: int = 0, limit: int = 10):
    items = crud.get_items(session, skip=skip, limit=limit)
    return [item[0] for item in items]
