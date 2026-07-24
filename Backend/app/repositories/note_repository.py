from bson import ObjectId
from datetime import datetime
from typing import List


def add_image_to_note(db, note_id: str, user_id: str, image_entry: dict) -> bool:
    """Thêm một ảnh mới vào danh sách images của Note.

    Args:
        note_id:     _id (str) của Note
        user_id:     _id (str) của user – dùng để xác nhận quyền sở hữu
        image_entry: dict ảnh (tạo bằng models.note.create_image_entry)

    Returns:
        True nếu thành công, False nếu không tìm thấy note hoặc không có quyền
    """
    try:
        result = db["notes"].update_one(
            {"_id": ObjectId(note_id), "user_id": user_id, "is_deleted": False},
            {
                "$push": {"images": image_entry},
                "$set":  {"updated_at": datetime.utcnow()}
            }
        )
        return result.matched_count > 0
    except Exception:
        return False


def get_note_images(db, note_id: str, user_id: str) -> List[dict]:
    """Lấy danh sách ảnh của một Note.

    Returns:
        Danh sách image dict, hoặc [] nếu không tìm thấy / không có quyền
    """
    try:
        note = db["notes"].find_one(
            {"_id": ObjectId(note_id), "user_id": user_id, "is_deleted": False},
            {"images": 1}
        )
        return note.get("images", []) if note else []
    except Exception:
        return []


def remove_image_from_note(db, note_id: str, user_id: str, image_url: str) -> bool:
    """Xoá một ảnh khỏi danh sách images của Note theo URL.

    Returns:
        True nếu thành công
    """
    try:
        result = db["notes"].update_one(
            {"_id": ObjectId(note_id), "user_id": user_id, "is_deleted": False},
            {
                "$pull": {"images": {"url": image_url}},
                "$set":  {"updated_at": datetime.utcnow()}
            }
        )
        return result.matched_count > 0
    except Exception:
        return False
