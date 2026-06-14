from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    buyer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CartItemRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CheckoutRequest(BaseModel):
    items: list[CartItemRequest]


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total: float
    status: str
    buyer_name: str | None = None


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    product_name: str | None = None
