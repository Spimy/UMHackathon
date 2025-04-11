from sqlmodel import SQLModel, Field
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
