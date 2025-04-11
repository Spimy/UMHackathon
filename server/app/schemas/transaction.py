from pydantic import BaseModel

class TransactionBase(BaseModel):
    item_id: str
    merchant_id: str
    order_time:str
    order_value: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
