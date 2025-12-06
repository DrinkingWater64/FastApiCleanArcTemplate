from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from uuid import uuid4, UUID
class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: Decimal
    stock: int

    created_at: Optional[datetime] = None
    last_modified_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

    def can_purchase(self, quantity: int) -> bool:
        return self.stock >= quantity

    def reduce_stock(self, quantity:int) -> None:
        if not self.can_purchase(quantity):
            raise ValueError("Insufficient stock")
        else:
            self.stock = self.stock - quantity

    