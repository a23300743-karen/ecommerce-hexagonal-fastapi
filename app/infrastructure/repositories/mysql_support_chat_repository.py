from datetime import datetime, timezone

from app.domain.models.support_conversation import SupportConversation
from app.domain.models.support_message import SupportMessage
from app.domain.ports.support_chat_repository import SupportChatRepository
from app.infrastructure.db.connection import get_connection


class MySQLSupportChatRepository(SupportChatRepository):

    def get_or_create_conversation(self, user_id: int) -> SupportConversation:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, c.user_id, u.name AS user_name, c.status,
                   c.created_at, c.updated_at
            FROM support_conversations c
            INNER JOIN users u ON u.id = c.user_id
            WHERE c.user_id=%s AND c.status='OPEN'
            ORDER BY c.id DESC LIMIT 1
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO support_conversations (user_id, status) VALUES (%s, 'OPEN')",
                (user_id,)
            )
            connection.commit()
            conversation_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return self.get_conversation(conversation_id)
        cursor.close()
        connection.close()
        return self._map_conversation(row)

    def get_conversation(self, conversation_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, c.user_id, u.name AS user_name, c.status,
                   c.created_at, c.updated_at
            FROM support_conversations c
            INNER JOIN users u ON u.id = c.user_id
            WHERE c.id=%s
            """,
            (conversation_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return self._map_conversation(row) if row else None

    def list_conversations(self):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, c.user_id, u.name AS user_name, c.status,
                   c.created_at, c.updated_at
            FROM support_conversations c
            INNER JOIN users u ON u.id = c.user_id
            ORDER BY c.updated_at DESC
            """
        )
        conversations = [self._map_conversation(row) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return conversations

    def save_message(self, message: SupportMessage):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO support_messages (conversation_id, sender_role, content)
            VALUES (%s, %s, %s)
            """,
            (message.conversation_id, message.sender_role, message.content)
        )
        connection.commit()
        message.id = cursor.lastrowid
        cursor.execute(
            "UPDATE support_conversations SET updated_at=CURRENT_TIMESTAMP WHERE id=%s",
            (message.conversation_id,)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return message

    def list_messages(self, conversation_id: int):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, conversation_id, sender_role, content, created_at
            FROM support_messages
            WHERE conversation_id=%s
            ORDER BY id
            """,
            (conversation_id,)
        )
        messages = [SupportMessage(**row) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return messages

    def _map_conversation(self, row):
        return SupportConversation(
            id=row["id"], user_id=row["user_id"], user_name=row["user_name"],
            status=row["status"], created_at=row["created_at"], updated_at=row["updated_at"]
        )
