from sqlmodel import select
from models.transaction import Transactions
from models import SessionDep


def create_transaction(session: SessionDep, tranaction_data: dict):
    db_transaction = Transactions(**tranaction_data)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


def get_transaction(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(Transactions).offset(skip).limit(limit)).all()
