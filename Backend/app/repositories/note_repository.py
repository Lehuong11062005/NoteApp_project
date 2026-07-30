from bson import ObjectId
from datetime import datetime
from typing import List
from app.config.database import get_database

class NoteRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["notes"]

    def create_note(self, note_data: dict) -> str:
        result = self.collection.insert_one(note_data)
        return str(result.inserted_id)

def add_image_to_note(db, note_id: str, user_id: str, image_entry: dict) -> bool:
    """Thêm một ảnh mới vào danh sách images của Note."""
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
    """Lấy danh sách ảnh của một Note."""
    try:
        note = db["notes"].find_one(
            {"_id": ObjectId(note_id), "user_id": user_id, "is_deleted": False},
            {"images": 1}
        )
        return note.get("images", []) if note else []
    except Exception:
        return []

def remove_image_from_note(db, note_id: str, user_id: str, image_url: str) -> bool:
    """Xoá một ảnh khỏi danh sách images của Note theo URL."""
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
