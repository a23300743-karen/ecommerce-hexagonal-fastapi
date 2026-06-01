from datetime import datetime, timezone

from app.domain.models.message import Message
from app.domain.ports.faq_port import FAQPort


class ChatService:

    def __init__(self, faq_provider: FAQPort):
        self.faq_provider = faq_provider

    def process_message(self, user: str, content: str):
        clean_content = content.strip()

        if not clean_content:
            raise ValueError("El mensaje no puede estar vacio")

        message = Message(
            id=None,
            user=user.strip() or "client",
            content=clean_content,
            created_at=datetime.now(timezone.utc)
        )

        faq_response = self.faq_provider.get_answer(clean_content)

        if faq_response:
            return {
                "type": "faq",
                "message": self._message_to_dict(message),
                "response": faq_response
            }

        return {
            "type": "support",
            "message": self._message_to_dict(message),
            "response": "Tu mensaje fue enviado a soporte. Un asistente lo revisara pronto."
        }

    def _message_to_dict(self, message: Message):
        return {
            "id": message.id,
            "user": message.user,
            "content": message.content,
            "created_at": message.created_at.isoformat()
        }
