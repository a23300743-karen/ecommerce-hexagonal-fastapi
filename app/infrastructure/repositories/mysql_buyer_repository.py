import mysql.connector

from app.domain.models.buyer_profile import BuyerProfile
from app.domain.ports.buyer_repository import BuyerRepository
from app.infrastructure.db.connection import get_connection


class MySQLBuyerRepository(BuyerRepository):

    def save(self, buyer: BuyerProfile) -> BuyerProfile:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO buyer_profiles
        (name, email, address, phone, status, user_id)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            buyer.name,
            buyer.email,
            buyer.address,
            buyer.phone,
            buyer.status,
            buyer.user_id
        )

        try:
            cursor.execute(sql, values)
            connection.commit()
        except mysql.connector.errors.IntegrityError as error:
            cursor.close()
            connection.close()
            raise ValueError("El correo ya existe") from error

        buyer.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return buyer

    def get_by_id(self, buyer_id: int):
        return self._get_one(
            """
            SELECT id, name, email, address, phone, status, user_id
            FROM buyer_profiles
            WHERE id=%s
            """,
            (buyer_id,)
        )

    def get_by_email(self, email: str):
        return self._get_one(
            """
            SELECT id, name, email, address, phone, status, user_id
            FROM buyer_profiles
            WHERE email=%s
            """,
            (email,)
        )

    def get_by_user_id(self, user_id: int):
        return self._get_one(
            """
            SELECT id, name, email, address, phone, status, user_id
            FROM buyer_profiles
            WHERE user_id=%s
            """,
            (user_id,)
        )

    def search_by_name(self, name: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, address, phone, status, user_id
            FROM buyer_profiles
            WHERE name LIKE %s
            """,
            (f"%{name}%",)
        )

        buyers = [self._map_row_to_buyer(row) for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return buyers

    def get_all(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, address, phone, status, user_id
            FROM buyer_profiles
            """
        )

        buyers = [self._map_row_to_buyer(row) for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return buyers

    def update(self, buyer_id: int, buyer: BuyerProfile):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE buyer_profiles
            SET name = %s,
                email = %s,
                address = %s,
                phone = %s,
                status = %s,
                user_id = %s
            WHERE id = %s
            """,
            (
                buyer.name,
                buyer.email,
                buyer.address,
                buyer.phone,
                buyer.status,
                buyer.user_id,
                buyer_id
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        return self.get_by_id(buyer_id)

    def change_status(self, buyer_id: int, status: str):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE buyer_profiles
            SET status = %s
            WHERE id = %s
            """,
            (status, buyer_id)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return self.get_by_id(buyer_id)

    def _get_one(self, sql: str, values: tuple):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, values)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row is None:
            return None

        return self._map_row_to_buyer(row)

    def _map_row_to_buyer(self, row) -> BuyerProfile:
        return BuyerProfile(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            address=row["address"],
            phone=row["phone"],
            status=row.get("status") or "ACTIVE",
            user_id=row.get("user_id")
        )
