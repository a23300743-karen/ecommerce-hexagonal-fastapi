from abc import ABC, abstractmethod
from app.domain.models.order import Order
from app.domain.models.order_item import OrderItem

class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def save_item(self, item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def get_all(self) -> list[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    def cancel(self, order_id: int) -> Order:
        pass