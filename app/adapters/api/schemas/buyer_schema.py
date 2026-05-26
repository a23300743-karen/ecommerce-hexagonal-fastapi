from pydantic import BaseModel, Field

class BuyerRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)
    address: str = Field(..., min_length=5)
    phone: str | None = None


class BuyerResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str | None = None
