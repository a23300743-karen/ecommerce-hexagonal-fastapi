from app.domain.models.order import Order
from app.domain.models.order_item import OrderItem
from app.domain.ports.order_repository import OrderRepository

class MemoryOrderRepository(OrderRepository):

    def __init__(self):
        self.orders = []
        self.items = []
        self.current_order_id = 1
        self.current_item_id = 1

    def save(self, order: Order) -> Order:
        order.id = self.current_order_id
        self.current_order_id += 1
        self.orders.append(order)
        return order

    def save_item(self, item: OrderItem) -> OrderItem:
        item.id = self.current_item_id
        self.current_item_id += 1
        self.items.append(item)
        return item

    def get_all(self):
        return self.orders

    def get_by_id(self, order_id: int):
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def get_items_by_order_id(self, order_id: int):
        return [
            item
            for item in self.items
            if item.order_id == order_id
        ]

    def cancel(self, order_id: int):
        order = self.get_by_id(order_id)

        if order is None:
            return None

        order.status = "CANCELLED"
        return order
