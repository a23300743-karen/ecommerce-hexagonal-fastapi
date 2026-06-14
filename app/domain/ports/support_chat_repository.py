from abc import ABC, abstractmethod
from app.domain.models.support_conversation import SupportConversation
from app.domain.models.support_message import SupportMessage


class SupportChatRepository(ABC):

    @abstractmethod
    def get_or_create_conversation(self, user_id: int) -> SupportConversation:
        pass

    @abstractmethod
    def get_conversation(self, conversation_id: int) -> SupportConversation | None:
        pass

    @abstractmethod
    def list_conversations(self) -> list[SupportConversation]:
        pass

    @abstractmethod
    def save_message(self, message: SupportMessage) -> SupportMessage:
        pass

    @abstractmethod
    def list_messages(self, conversation_id: int) -> list[SupportMessage]:
        pass
