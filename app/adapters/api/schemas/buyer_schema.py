from pydantic import BaseModel

class BuyerRequest(BaseModel):
    name: str
    email: str
    address: str
    phone: str | None = None


class BuyerResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str | None = None