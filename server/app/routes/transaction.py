from fastapi import APIRouter
import crud
from schemas import Transaction, TransactionCreate
from models import SessionDep

router = APIRouter(tags=["transactions"])


@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, session: SessionDep):
    return crud.create_transaction(session, transaction.dict())


@router.get("/transactions/", response_model=list[Transaction])
def read_transactions(session: SessionDep, skip: int = 0, limit: int = 10):
    transactions = crud.get_transaction(session, skip=skip, limit=limit)
    return [transaction[0] for transaction in transactions]
