from pydantic import BaseModel
from typing import Optional, List


class TransactionsItemsBase(BaseModel):
    id: str
    item_id: str
    merchant_id: str

class TransactionItemsCreate(TransactionsItemsBase):
    pass

class Transaction(TransactionsItemsBase):
    id: int

    class Config:
        orm_mode = True


class TransactionDataBase(BaseModel):
    order_id: str
    order_time: str
    driver_arrival_time: str
    driver_pickup_time: str
    delivery_time: str
    order_value: float
    eater_id: str
    merchant_id: str

class TransactionDataCreate(TransactionDataBase):
    pass

class TransactionData(TransactionDataBase):
    id: Optional[str]

    class Config:
        orm_mode = True


class MerchantTransactionSummaryItem(BaseModel):
    item_id: str
    frequency: int
    total_value: float


class MerchantTransactionSummary(BaseModel):
    today: List[MerchantTransactionSummaryItem]
    this_week: List[MerchantTransactionSummaryItem]
    this_month: List[MerchantTransactionSummaryItem]

