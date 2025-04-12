from sqlmodel import select
from models.item import Item
from models import SessionDep


def create_item(session: SessionDep, item_data: dict):
    db_item = Item(**item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_items(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(Item).offset(skip).limit(limit)).all()

