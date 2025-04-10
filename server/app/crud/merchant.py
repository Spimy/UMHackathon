from models.merchant import Merchant, User
from models import SessionDep
from sqlmodel import select


def create_merchant(session: SessionDep, merchant_data: dict):
    db_merchant = Merchant(**merchant_data)
    session.add(db_merchant)
    session.commit()
    session.refresh(db_merchant)
    return db_merchant


def get_merchants(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(Merchant).offset(skip).limit(limit)).all()


def get_user(session: SessionDep, email: str):
    return session.execute(select(User).where(User.user_email == email)).first()
