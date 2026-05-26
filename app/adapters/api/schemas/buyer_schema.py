from pydantic import BaseModel, Field


class BuyerRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=5)
    address: str = Field(..., min_length=1)
    phone: str | None = None


class BuyerUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=5)
    address: str = Field(..., min_length=1)
    phone: str | None = None
    status: str = "ACTIVE"


class BuyerResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str | None = None
    status: str = "ACTIVE"
