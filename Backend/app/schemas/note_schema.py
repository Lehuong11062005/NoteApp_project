from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, example="My Note Title", description="Tiêu đề ghi chú")
    content: str = Field(..., description="Nội dung ghi chú")
    category: Optional[str] = "Chung"
    priority: Optional[str] = "Bình Thường"
    image_url: Optional[str] = None
    reminder_time: Optional[datetime] = None
    user_id: Optional[str] = None

