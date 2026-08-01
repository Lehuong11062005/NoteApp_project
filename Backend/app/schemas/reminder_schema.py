from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReminderCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    reminder_time: datetime
    status: Optional[str] = "pending"
    user_id: Optional[str] = None
    note_id: Optional[str] = None


class ReminderUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_time: Optional[datetime] = None
    status: Optional[str] = None
