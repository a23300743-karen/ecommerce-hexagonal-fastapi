from pydantic import BaseModel

class OrderRequest(BaseModel):
    buyer_id: int
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total: float
    status: str