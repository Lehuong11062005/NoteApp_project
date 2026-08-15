from datetime import datetime, timezone
from typing import Optional

def create_notification_document(
    user_id: str,
    title: str,
    message: str,
    notification_type: str = "reminder",
    source_id: Optional[str] = None
) -> dict:
    """Tạo document Notification chuẩn cho MongoDB collection 'notifications'."""
    return {
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": notification_type,
        "source_id": source_id,
        "is_read": False,
        "created_at": datetime.now(timezone.utc),
        "read_at": None
    }
