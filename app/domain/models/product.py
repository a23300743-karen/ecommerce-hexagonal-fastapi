from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    stock: int
    status: str = "ACTIVE"