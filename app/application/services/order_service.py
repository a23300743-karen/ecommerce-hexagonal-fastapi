from app.domain.models.order import Order
from app.domain.models.order_item import OrderItem
from app.domain.ports.order_repository import OrderRepository
from app.domain.ports.product_repository import ProductRepository
from app.domain.ports.buyer_repository import BuyerRepository


class OrderService:

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        buyer_repository: BuyerRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.buyer_repository = buyer_repository

    def create_order(self, buyer_id: int, product_id: int, quantity: int) -> Order:
        buyer = self.buyer_repository.get_by_id(buyer_id)

        if buyer is None:
            raise ValueError("El perfil de compra no existe")

        if buyer.status != "ACTIVE":
            raise ValueError("El perfil de compra no esta activo")

        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise ValueError("El producto no existe")

        if product.status != "ACTIVE":
            raise ValueError("El producto no esta activo")

        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        if product.stock < quantity:
            raise ValueError("No hay stock suficiente")

        total = product.price * quantity

        product.stock -= quantity
        self.product_repository.update_stock(product.id, product.stock)

        order = Order(
            id=0,
            buyer_id=buyer_id,
            total=total,
            status="CREATED"
        )

        saved_order = self.order_repository.save(order)

        item = OrderItem(
            id=0,
            order_id=saved_order.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price,
            subtotal=total
        )

        self.order_repository.save_item(item)

        return saved_order

    def list_orders(self):
        return self.order_repository.get_all()

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)

        if order is None:
            raise ValueError("La orden no existe")

        return order

    def get_order_items(self, order_id: int) -> list[OrderItem]:
        self.get_order(order_id)
        return self.order_repository.get_items_by_order_id(order_id)

    def cancel_order(self, order_id: int):
        order = self.order_repository.get_by_id(order_id)

        if order is None:
            raise ValueError("La orden no existe")

        if order.status == "CANCELLED":
            raise ValueError("La orden ya esta cancelada")

        items = self.order_repository.get_items_by_order_id(order_id)

        for item in items:
            product = self.product_repository.get_by_id(item.product_id)

            if product is not None:
                self.product_repository.update_stock(
                    product.id,
                    product.stock + item.quantity
                )

        return self.order_repository.cancel(order_id)
