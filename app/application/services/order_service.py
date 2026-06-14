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

    def checkout(self, user_id: int, items: list[dict]) -> Order:
        buyer = self.buyer_repository.get_by_user_id(user_id)

        if buyer is None:
            raise ValueError("No existe perfil de comprador para este usuario")

        if buyer.status != "ACTIVE":
            raise ValueError("El perfil de compra no esta activo")

        if not items:
            raise ValueError("El carrito esta vacio")

        total = 0
        prepared_items = []

        for item in items:
            product_id = int(item["product_id"])
            quantity = int(item["quantity"])

            if quantity <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")

            product = self.product_repository.get_by_id(product_id)

            if product is None:
                raise ValueError("El producto no existe")

            if product.status != "ACTIVE":
                raise ValueError("El producto no esta activo")

            if product.stock < quantity:
                raise ValueError(f"No hay stock suficiente para {product.name}")

            subtotal = product.price * quantity
            total += subtotal

            prepared_items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal
                }
            )

        order = Order(
            id=0,
            buyer_id=buyer.id,
            total=total,
            status="CREATED"
        )

        saved_order = self.order_repository.save(order)

        for prepared_item in prepared_items:
            product = prepared_item["product"]
            quantity = prepared_item["quantity"]
            subtotal = prepared_item["subtotal"]

            self.product_repository.update_stock(product.id, product.stock - quantity)

            order_item = OrderItem(
                id=0,
                order_id=saved_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                subtotal=subtotal
            )

            self.order_repository.save_item(order_item)

        return saved_order

    def create_order(self, buyer_id: int, product_id: int, quantity: int) -> Order:
        buyer = self.buyer_repository.get_by_id(buyer_id)

        if buyer is None:
            raise ValueError("El perfil de compra no existe")

        if buyer.status != "ACTIVE":
            raise ValueError("El perfil de compra no esta activo")

        return self.checkout_from_buyer(buyer.id, product_id, quantity)

    def checkout_from_buyer(self, buyer_id: int, product_id: int, quantity: int) -> Order:
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
        self.product_repository.update_stock(product.id, product.stock - quantity)

        order = Order(id=0, buyer_id=buyer_id, total=total, status="CREATED")
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

    def list_orders_for_user(self, user_id: int):
        buyer = self.buyer_repository.get_by_user_id(user_id)

        if buyer is None:
            raise ValueError("No existe perfil de comprador para este usuario")

        return self.order_repository.get_by_buyer_id(buyer.id)

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)

        if order is None:
            raise ValueError("La orden no existe")

        return order

    def get_order_for_user(self, user_id: int, order_id: int) -> Order:
        buyer = self.buyer_repository.get_by_user_id(user_id)

        if buyer is None:
            raise ValueError("No existe perfil de comprador para este usuario")

        order = self.get_order(order_id)

        if order.buyer_id != buyer.id:
            raise ValueError("La orden no pertenece al usuario actual")

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
