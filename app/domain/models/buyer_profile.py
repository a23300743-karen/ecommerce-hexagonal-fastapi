from dataclasses import dataclass

@dataclass
class BuyerProfile:
    id: int
    name: str
    email: str
    address: str
    phone: str | None = None
    status: str = "ACTIVE"
