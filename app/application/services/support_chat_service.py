from datetime import datetime, timezone

from app.domain.models.support_message import SupportMessage
from app.domain.ports.faq_port import FAQPort
from app.domain.ports.support_chat_repository import SupportChatRepository


class SupportChatService:

    def __init__(self, repository: SupportChatRepository, faq_provider: FAQPort):
        self.repository = repository
        self.faq_provider = faq_provider

    def receive_customer_message(self, user_id: int, content: str):
        clean_content = content.strip()
        if not clean_content:
            raise ValueError("El mensaje no puede estar vacio")
        conversation = self.repository.get_or_create_conversation(user_id)
        customer_message = self._save(conversation.id, "CUSTOMER", clean_content)
        answer = self.faq_provider.get_answer(clean_content)
        if answer is None:
            answer = (
                "No encontre una respuesta automatica para esa pregunta, "
                "pero tu mensaje ya fue enviado al administrador."
            )
        automatic_message = self._save(conversation.id, "ASSISTANT", answer)
        return conversation, customer_message, automatic_message

    def send_admin_message(self, conversation_id: int, content: str):
        if self.repository.get_conversation(conversation_id) is None:
            raise ValueError("La conversacion no existe")
        clean_content = content.strip()
        if not clean_content:
            raise ValueError("El mensaje no puede estar vacio")
        return self._save(conversation_id, "ADMIN", clean_content)

    def get_or_create_conversation(self, user_id: int):
        return self.repository.get_or_create_conversation(user_id)

    def get_conversation(self, conversation_id: int):
        return self.repository.get_conversation(conversation_id)

    def list_conversations(self):
        return self.repository.list_conversations()

    def list_messages(self, conversation_id: int):
        if self.repository.get_conversation(conversation_id) is None:
            raise ValueError("La conversacion no existe")
        return self.repository.list_messages(conversation_id)

    def _save(self, conversation_id: int, sender_role: str, content: str):
        return self.repository.save_message(SupportMessage(
            id=0, conversation_id=conversation_id, sender_role=sender_role,
            content=content, created_at=datetime.now(timezone.utc)
        ))
