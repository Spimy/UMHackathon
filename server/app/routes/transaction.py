from fastapi import APIRouter, Depends
import crud
from schemas import MerchantTransactionSummary
from models import SessionDep

router = APIRouter(tags=["transactions"])

@router.get("/transactions/{merchant_id}/summary", response_model=MerchantTransactionSummary)
def get_merchant_summary(
    merchant_id: str,
    session: SessionDep
):
    return crud.get_merchant_transactions_summary(session, merchant_id)

