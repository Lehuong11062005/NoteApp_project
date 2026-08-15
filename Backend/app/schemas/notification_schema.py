from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificationCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    type: Optional[str] = "reminder"
    source_id: Optional[str] = None
    user_id: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str = "reminder"
    source_id: Optional[str] = None
    is_read: bool = False
    created_at: Optional[str] = None
    read_at: Optional[str] = None

class UnreadCountResponse(BaseModel):
    unread_count: int
