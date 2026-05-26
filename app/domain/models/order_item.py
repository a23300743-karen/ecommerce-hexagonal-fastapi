from dataclasses import dataclass

@dataclass
class OrderItem:
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float