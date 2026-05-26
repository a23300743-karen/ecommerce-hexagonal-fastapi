from pydantic import BaseModel

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    status: str