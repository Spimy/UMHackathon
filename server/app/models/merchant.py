from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import string
import random


def generate_merchant_id() -> str:
    # Use lowercase letters and digits
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=5))


class Merchant(SQLModel, table=True):
    merchant_id: str = Field(
        default_factory=generate_merchant_id, primary_key=True
    )
    merchant_name: str
    join_date: str
    city_id: int

    users: list['User'] = Relationship(back_populates="merchant")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_email: str

    merchant_id: str | None = Field(
        default=None, foreign_key="merchant.merchant_id"
    )
    merchant: Merchant | None = Relationship(back_populates="users")
