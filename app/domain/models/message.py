from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Message:
    id: Optional[int]
    user: str
    content: str
    created_at: datetime
