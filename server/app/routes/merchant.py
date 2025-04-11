from fastapi import APIRouter
import crud
from schemas import Merchant, MerchantCreate
from models import SessionDep

router = APIRouter(tags=["merchants"])


@router.post("/merchants/", response_model=Merchant)
def create_merchant(merchant: MerchantCreate, session: SessionDep):
    return crud.create_merchant(session, merchant.dict())


@router.get("/merchants/", response_model=list[Merchant])
def read_merchants(session: SessionDep, skip: int = 0, limit: int = 10):
    merchants = crud.get_merchants(session, skip=skip, limit=limit)
    return [merchant[0] for merchant in merchants]
