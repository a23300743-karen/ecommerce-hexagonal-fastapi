import mysql.connector

from app.domain.models.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.db.connection import get_connection


class MySQLUserRepository(UserRepository):

    def save(self, user: User) -> User:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO users
        (name, email, password_hash, role, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            user.name,
            user.email,
            user.password_hash,
            user.role,
            user.status
        )

        try:

            cursor.execute(sql, values)
            connection.commit()

        except mysql.connector.errors.IntegrityError as error:

            cursor.close()
            connection.close()

            raise ValueError("El correo ya esta registrado") from error

        user.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return user

    def get_by_email(self, email: str):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role, status
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row is None:
            return None

        return self._map_row_to_user(row)

    def get_by_id(self, user_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role, status
            FROM users
            WHERE id=%s
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row is None:
            return None

        return self._map_row_to_user(row)

    def _map_row_to_user(self, row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"],
            status=row["status"]
        )
