from app.domain.models.product import Product
from app.domain.ports.product_repository import ProductRepository
from app.infrastructure.db.connection import get_connection


class MySQLProductRepository(ProductRepository):

    def save(self, product: Product) -> Product:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO products (name, description, price, stock, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            product.name,
            product.description,
            product.price,
            product.stock,
            product.status
        )

        cursor.execute(sql, values)
        connection.commit()

        product.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return product

    def get_all(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id, name, description, price, stock, status FROM products")

        products = [
            self._map_row_to_product(row)
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return products

    def get_by_id(self, product_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, name, description, price, stock, status FROM products WHERE id = %s",
            (product_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row is None:
            return None

        return self._map_row_to_product(row)

    def search_by_name(self, name: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, description, price, stock, status
            FROM products
            WHERE name LIKE %s
            """,
            (f"%{name}%",)
        )

        products = [
            self._map_row_to_product(row)
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return products

    def update(self, product_id: int, product: Product):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE products
            SET name = %s,
                description = %s,
                price = %s,
                stock = %s,
                status = %s
            WHERE id = %s
            """,
            (
                product.name,
                product.description,
                product.price,
                product.stock,
                product.status,
                product_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return self.get_by_id(product_id)

    def update_stock(self, product_id: int, stock: int):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE products SET stock = %s WHERE id = %s",
            (stock, product_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return self.get_by_id(product_id)

    def change_status(self, product_id: int, status: str):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE products SET status = %s WHERE id = %s",
            (status, product_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return self.get_by_id(product_id)

    def _map_row_to_product(self, row) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            description=row["description"] or "",
            price=float(row["price"]),
            stock=row["stock"],
            status=row["status"]
        )
