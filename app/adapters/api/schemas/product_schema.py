from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str = Field(..., min_length=2)
    description: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    status: str
