from dataclasses import dataclass
from datetime import datetime


@dataclass
class SupportConversation:
    id: int
    user_id: int
    user_name: str
    status: str
    created_at: datetime
    updated_at: datetime
