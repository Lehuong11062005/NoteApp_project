from datetime import datetime
from typing import List

def create_note_document(user_id: str, title: str, content: str = "",
                         images: List[dict] = None,
                         tags: List[str] = None,
                         category: str = None) -> dict:
    """Tạo document Note theo đúng cấu trúc lưu vào MongoDB collection 'notes'.

    Args:
        user_id:  _id (str) của user sở hữu ghi chú
        title:    Tiêu đề ghi chú
        content:  Nội dung ghi chú
        images:   Danh sách ảnh đính kèm, mỗi phần tử là dict:
                  { "url": "...", "thumb_url": "...", "delete_url": "...",
                    "filename": "...", "uploaded_at": datetime }
        tags:     Danh sách nhãn (auto-tag hoặc thủ công)
        category: Tên danh mục
    """
    return {
        "user_id": user_id,                     # ID chủ sở hữu
        "title": title,                         # Tiêu đề ghi chú
        "content": content,                     # Nội dung (text)
        "images": images or [],                 # Danh sách ảnh đính kèm (ImgBB URLs)
        "tags": tags or [],                     # Nhãn ghi chú
        "category": category,                   # Danh mục
        "is_deleted": False,                    # Soft delete flag
        "created_at": datetime.utcnow(),        # Thời điểm tạo (UTC)
        "updated_at": datetime.utcnow(),        # Thời điểm cập nhật (UTC)
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
