from datetime import datetime
from typing import Any, Dict, List, Optional
from bson import ObjectId
from app.repositories.note_repository import NoteRepository
from app.schemas.note_schema import NoteCreateSchema


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()

    def create_note(self, note_data: NoteCreateSchema, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Tạo ghi chú mới."""
        # Hỗ trợ cả Pydantic v1 (dict) và v2 (model_dump)
        data = note_data.model_dump() if hasattr(note_data, "model_dump") else note_data.dict()
        
        now = datetime.now()
        data["create_at"] = now
        data["update_at"] = now
        
        # Ưu tiên user_id truyền từ tham số (token/auth) nếu schema không có
        data["user_id"] = getattr(note_data, "user_id", None) or user_id

        if not data.get("user_id"):
            raise ValueError("user_id là bắt buộc")

        note_id = self.note_repo.create_note(data)
        return {
            "id": note_id,
            "message": "Tạo ghi chú thành công"
        }

    def get_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Lấy ghi chú theo ID."""
        if not ObjectId.is_valid(note_id):
            raise ValueError("ID ghi chú không hợp lệ")
            
        return self.note_repo.get_note_by_id(note_id)

    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Lấy toàn bộ ghi chú trong hệ thống."""
        return self.note_repo.get_all_notes()

    def get_notes_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Lấy danh sách ghi chú theo user_id."""
        if not user_id:
            raise ValueError("user_id là bắt buộc")
        return self.note_repo.get_notes_by_user(user_id)

    def search_notes_by_user(self, user_id: str, keyword: str) -> List[Dict[str, Any]]:
        """Tìm kiếm ghi chú của user theo từ khóa."""
        if not user_id:
            raise ValueError("user_id là bắt buộc")
        return self.note_repo.search_notes_by_user(user_id, keyword)

    def update_note(
        self, 
        note_id: str, 
        note_data: NoteCreateSchema, 
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cập nhật nội dung ghi chú."""
        if not ObjectId.is_valid(note_id):
            raise ValueError("ID ghi chú không hợp lệ")

        # Chỉ lấy các trường được gửi lên để update (exclude_unset=True)
        if hasattr(note_data, "model_dump"):
            update_data = note_data.model_dump(exclude_unset=True)
        else:
            update_data = note_data.dict(exclude_unset=True)

        if not update_data:
            return {"message": "Không có dữ liệu để cập nhật"}

        update_data["update_at"] = datetime.now()
        if user_id:
            update_data["user_id"] = user_id

        updated = self.note_repo.update_note(note_id, update_data)
        if not updated:
            raise ValueError("Không tìm thấy ghi chú để cập nhật")

        return {
            "id": note_id,
            "message": "Cập nhật ghi chú thành công"
        }

    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Xóa ghi chú theo ID."""
        if not ObjectId.is_valid(note_id):
            raise ValueError("ID ghi chú không hợp lệ")

        deleted = self.note_repo.delete_note(note_id)
        if not deleted:
            raise ValueError("Không tìm thấy ghi chú để xóa")

        return {
            "id": note_id,
            "message": "Xóa ghi chú thành công"
        }