from pydantic import BaseModel


class MerchantBase(BaseModel):
    merchant_name: str
    join_date: str
    city_id: int


class MerchantCreate(MerchantBase):
    pass


class Merchant(MerchantBase):
    merchant_id: int

    class Config:
        orm_mode = True
