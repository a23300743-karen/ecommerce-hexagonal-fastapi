from app.domain.models.buyer_profile import BuyerProfile
from app.domain.ports.buyer_repository import BuyerRepository
from app.infrastructure.db.connection import get_connection

class MySQLBuyerRepository(BuyerRepository):

    def save(
        self,
        buyer: BuyerProfile
    ) -> BuyerProfile:

        connection = get_connection()

        cursor = connection.cursor()

        sql = """
        INSERT INTO buyer_profiles
        (
            name,
            email,
            address,
            phone
        )
        VALUES
        (%s,%s,%s,%s)
        """

        values = (
            buyer.name,
            buyer.email,
            buyer.address,
            buyer.phone
        )

        cursor.execute(
            sql,
            values
        )

        connection.commit()

        buyer.id = cursor.lastrowid

        cursor.close()

        connection.close()

        return buyer

    def get_by_id(
        self,
        buyer_id: int
    ):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                address,
                phone
            FROM buyer_profiles
            WHERE id=%s
            """,
            (
                buyer_id,
            )
        )

        row = cursor.fetchone()

        cursor.close()

        connection.close()

        if row is None:

            return None

        return BuyerProfile(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            address=row["address"],
            phone=row["phone"]
        )

    def get_all(self):

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                address,
                phone
            FROM buyer_profiles
            """
        )

        buyers = []

        for row in cursor.fetchall():

            buyers.append(
                BuyerProfile(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    address=row["address"],
                    phone=row["phone"]
                )
            )

        cursor.close()

        connection.close()

        return buyers