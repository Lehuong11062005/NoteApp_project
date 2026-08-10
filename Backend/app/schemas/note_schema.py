from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# 1. Định nghĩa các Enum để quản lý chặt chẽ giá trị
class PriorityEnum(str, Enum):
    HIGH = "Cao"
    NORMAL = "Bình Thường"
    LOW = "Thấp"

class NoteStatusEnum(str, Enum):
    PENDING = "Đang chờ"
    COMPLETED = "Đã hoàn thành"
    OVERDUE = "Quá hạn"

class NoteCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, examples=["My Note Title"])
    content: str = Field(..., description="Nội dung ghi chú")
    category: str = Field(default="Chung")
    priority: PriorityEnum = Field(default=PriorityEnum.NORMAL)
    
    # 2. Thêm trường status với giá trị mặc định khi tạo mới luôn là "Đang chờ"
    status: NoteStatusEnum = Field(default=NoteStatusEnum.PENDING)
    
    image_url: Optional[str] = None
    reminder_time: Optional[datetime] = None