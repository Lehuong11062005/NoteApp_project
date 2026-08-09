from datetime import datetime
from typing import Any, Dict, List, Optional
from bson import ObjectId
from app.config.database import get_database


class NoteRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["notes"]

    @staticmethod
    def _to_object_id(note_id: str) -> Optional[ObjectId]:
        """Chuyển đổi string id sang ObjectId an toàn."""
        try:
            return ObjectId(note_id)
        except Exception:
            return None

    @staticmethod
    def _format_note(note: Dict[str, Any]) -> Dict[str, Any]:
        """Chuẩn hóa dữ liệu note trả về: ép kiểu _id và datetime sang string."""
        if not note:
            return note
        
        note["_id"] = str(note["_id"])
        
        # Chuyển đổi timestamp sang định dạng ISO string
        for field in ["create_at", "update_at", "created_at", "updated_at"]:
            if note.get(field) is not None and isinstance(note[field], datetime):
                note[field] = note[field].isoformat()
                
        return note

    def create_note(self, note_data: dict) -> str:
        """Tạo mới một note."""
        if "created_at" not in note_data and "create_at" not in note_data:
            note_data["create_at"] = datetime.now()
            
        result = self.collection.insert_one(note_data)
        return str(result.inserted_id)

    def get_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Lấy chi tiết note theo ID."""
        obj_id = self._to_object_id(note_id)
        if not obj_id:
            return None

        note = self.collection.find_one({"_id": obj_id})
        return self._format_note(note) if note else None

    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả các note."""
        notes = list(self.collection.find())
        return [self._format_note(note) for note in notes]

    def get_notes_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Lấy danh sách note theo user_id."""
        cursor = self.collection.find({"user_id": user_id})
        return [self._format_note(item) for item in cursor]

    def search_notes_by_user(self, user_id: str, keyword: str) -> List[Dict[str, Any]]:
        """Tìm kiếm note của user theo từ khóa."""
        query: Dict[str, Any] = {"user_id": user_id}
        normalized_keyword = (keyword or "").strip()
        if normalized_keyword:
            query["$or"] = [
                {"title": {"$regex": normalized_keyword, "$options": "i"}},
                {"content": {"$regex": normalized_keyword, "$options": "i"}},
                {"category": {"$regex": normalized_keyword, "$options": "i"}},
                {"priority": {"$regex": normalized_keyword, "$options": "i"}},
            ]

        cursor = self.collection.find(query)
        return [self._format_note(item) for item in cursor]

    def update_note(self, note_id: str, update_data: dict) -> bool:
        """Cập nhật thông tin note."""
        obj_id = self._to_object_id(note_id)
        if not obj_id:
            return False

        if "update_at" not in update_data and "updated_at" not in update_data:
            update_data["update_at"] = datetime.now()

        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_note(self, note_id: str) -> bool:
        """Xóa note theo ID."""
        obj_id = self._to_object_id(note_id)
        if not obj_id:
            return False

        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0