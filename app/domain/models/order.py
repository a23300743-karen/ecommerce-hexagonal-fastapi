from dataclasses import dataclass

@dataclass
class Order:
    id: int
    buyer_id: int
    total: float
    status: str