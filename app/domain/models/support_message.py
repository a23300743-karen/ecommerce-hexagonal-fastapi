from dataclasses import dataclass
from datetime import datetime


@dataclass
class SupportMessage:
    id: int
    conversation_id: int
    sender_role: str
    content: str
    created_at: datetime
