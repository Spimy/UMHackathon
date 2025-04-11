from pydantic import BaseModel


class MerchantBase(BaseModel):
    merchant_name: str
    join_date: str
    city_id: int


class MerchantCreate(MerchantBase):
    pass


class Merchant(MerchantBase):
    merchant_id: str

    class Config:
        orm_mode = True
    
class MerchantName(BaseModel):
    merchant_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_email: str
    merchant_id: str


class User(UserBase):
    id: int
    merchant: Merchant

    class Config:
        orm_mode = True
