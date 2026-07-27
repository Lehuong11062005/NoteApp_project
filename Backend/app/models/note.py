from datetime import datetime
from typing import List, Optional

def create_note_document(user_id: str, title: str, content: str = "",
                         images: List[dict] = None,
                         tags: List[str] = None,
                         category: str = None) -> dict:
    """Tạo document Note chuẩn cho MongoDB collection 'notes'."""
    return {
        "user_id": user_id,
        "title": title,
        "content": content,
        "images": images or [],
        "tags": tags or [],
        "category": category,
        "is_deleted": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

def create_image_entry(url: str, thumb_url: str = None,
                       delete_url: str = None, filename: str = None,
                       width: int = None, height: int = None,
                       size: int = None) -> dict:
    """Tạo dict chuẩn cho một ảnh đính kèm trong Note.images."""
    return {
        "url": url,
        "thumb_url": thumb_url,
        "delete_url": delete_url,
        "filename": filename,
        "width": width,
        "height": height,
        "size": size,
        "uploaded_at": datetime.utcnow(),
    }
