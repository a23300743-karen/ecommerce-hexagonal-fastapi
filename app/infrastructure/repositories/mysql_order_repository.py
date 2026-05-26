from app.domain.models.order import Order
from app.domain.models.order_item import OrderItem
from app.domain.ports.order_repository import OrderRepository
from app.infrastructure.db.connection import get_connection

class MySQLOrderRepository(OrderRepository):

    def save(self, order: Order) -> Order:

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO purchase_orders
        (
            buyer_id,
            status,
            total
        )
        VALUES
        (%s,%s,%s)
        """

        values = (
            order.buyer_id,
            order.status,
            order.total
        )

        cursor.execute(
            sql,
            values
        )

        connection.commit()

        order.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return order

    def save_item(
        self,
        item: OrderItem
    ) -> OrderItem:

        connection = get_connection()

        cursor = connection.cursor()

        sql = """
        INSERT INTO order_items
        (
            order_id,
            product_id,
            quantity,
            unit_price,
            subtotal
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """

        values = (
            item.order_id,
            item.product_id,
            item.quantity,
            item.unit_price,
            item.subtotal
        )

        cursor.execute(
            sql,
            values
        )

        connection.commit()

        item.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return item

    def get_all(self):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                buyer_id,
                total,
                status
            FROM purchase_orders
            """
        )

        orders = []

        for row in cursor.fetchall():

            orders.append(
                Order(
                    id=row["id"],
                    buyer_id=row["buyer_id"],
                    total=float(row["total"]),
                    status=row["status"]
                )
            )

        cursor.close()
        connection.close()

        return orders

    def get_by_id(
        self,
        order_id: int
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                buyer_id,
                total,
                status
            FROM purchase_orders
            WHERE id=%s
            """,
            (
                order_id,
            )
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row is None:

            return None

        return Order(
            id=row["id"],
            buyer_id=row["buyer_id"],
            total=float(row["total"]),
            status=row["status"]
        )

    def get_items_by_order_id(
        self,
        order_id: int
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                order_id,
                product_id,
                quantity,
                unit_price,
                subtotal
            FROM order_items
            WHERE order_id=%s
            """,
            (
                order_id,
            )
        )

        items = []

        for row in cursor.fetchall():

            items.append(
                OrderItem(
                    id=row["id"],
                    order_id=row["order_id"],
                    product_id=row["product_id"],
                    quantity=row["quantity"],
                    unit_price=float(row["unit_price"]),
                    subtotal=float(row["subtotal"])
                )
            )

        cursor.close()
        connection.close()

        return items

    def cancel(
        self,
        order_id: int
    ) -> Order:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE purchase_orders
            SET status='CANCELLED'
            WHERE id=%s
            """,
            (
                order_id,
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return self.get_by_id(
            order_id
        )
    
