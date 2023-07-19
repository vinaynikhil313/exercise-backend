import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, condecimal, conint, constr, root_validator
from sqlmodel import SQLModel, Field


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(Enum):
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILURE = 2


class Order(SQLModel, table=True):

    __tablename__ = "orders"

    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                    primary_key=True,
                    index=True,
                    nullable=False)
    created_at: datetime

    type: OrderType = Field(..., alias="type", sa_column_kwargs={"name": "order_type"})
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)]
    quantity: conint(gt=0)
    status: OrderStatus = Field(default=OrderStatus.IN_PROGRESS)


class CreateOrderModel(BaseModel):
    type_: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)]
    quantity: conint(gt=0)

    @root_validator
    def validator(cls, values: dict):
        if values.get("type_") == "market" and values.get("limit_price"):
            raise ValueError(
                "Providing a `limit_price` is prohibited for type `market`"
            )

        if values.get("type_") == "limit" and not values.get("limit_price"):
            raise ValueError("Attribute `limit_price` is required for type `limit`")

        return values

    def to_order_entity(self) -> Order:
        entity = Order()
        entity.type = self.type_
        entity.side = self.side
        entity.instrument = self.instrument
        entity.limit_price = self.limit_price
        entity.quantity = self.quantity
        entity.created_at = datetime.utcnow()

        return entity


class CreateOrderResponseModel(Order):
    pass
