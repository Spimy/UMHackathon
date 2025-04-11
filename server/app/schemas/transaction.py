from pydantic import BaseModel

class TransactionBase(BaseModel):
    item_id: str
    merchant_id: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
