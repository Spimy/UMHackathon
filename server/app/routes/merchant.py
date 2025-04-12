from fastapi import APIRouter, HTTPException
import crud
from schemas import Merchant, MerchantCreate, User, Item
from models import SessionDep

router = APIRouter(tags=["merchants"])


@router.post("/merchants/", response_model=Merchant)
def create_merchant(merchant: MerchantCreate, session: SessionDep):
    return crud.create_merchant(session, merchant.dict())


@router.get("/merchants/", response_model=list[Merchant])
def read_merchants(session: SessionDep, skip: int = 0, limit: int = 10):
    merchants = crud.get_merchants(session, skip=skip, limit=limit)
    return [merchant[0] for merchant in merchants]


@router.get('/user/', response_model=User)
def read_merchant(email: str, session: SessionDep):
    user = crud.get_user(session, email)
    print(f"spimy-test: {user}")

    if user is not None:
        user = user.tuple()[0]
        return {
            'id': user.id,
            'user_email': user.user_email,
            'merchant_id': user.merchant_id,
            'merchant': user.merchant
        }

    raise HTTPException(status_code=404, detail="User not found")


@router.get("/merchants/{merchant_id}/items", response_model=list[Item])
def read_items_by_merchant(merchant_id: str, session: SessionDep):
    items = crud.get_items_by_merchant(session, merchant_id)
    return [item[0] for item in items]

