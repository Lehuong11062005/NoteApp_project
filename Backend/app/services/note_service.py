from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import Depends
from app.repositories.note_repository import NoteRepository
from app.schemas.note_schema import NoteCreateSchema, NoteStatusEnum
from app.utils.datetime_helper import (
    get_utc_now,
    parse_vietnam_datetime_to_utc
)


class NoteService:
    def __init__(self, note_repo: NoteRepository = Depends()):
        self.note_repo = note_repo

    def _process_dynamic_status(self, note: Dict[str, Any]) -> Dict[str, Any]:
        """Hàm nội bộ để tính toán động trạng thái Quá hạn theo chuẩn múi giờ Việt Nam."""
        if not note:
            return note
            
        reminder_time = note.get("reminder_time")
        current_status = note.get("status")
        
        if current_status == NoteStatusEnum.PENDING and reminder_time:
            reminder_dt = parse_vietnam_datetime_to_utc(reminder_time)
            if reminder_dt and get_utc_now() > reminder_dt:
                note["status"] = NoteStatusEnum.OVERDUE
                # Cập nhật ngầm xuống DB
                self.note_repo.update_note(note["_id"], {"status": NoteStatusEnum.OVERDUE})
                
        return note

    def create_note(self, note_data: NoteCreateSchema, user_id: str) -> Dict[str, Any]:
        """Tạo ghi chú mới."""
        data = note_data.model_dump()
        now = datetime.now(timezone.utc)
        
        data["create_at"] = now
        data["update_at"] = now
        data["user_id"] = user_id
        data["status"] = NoteStatusEnum.PENDING

        note_id = self.note_repo.create_note(data)
        return {"id": note_id, "message": "Tạo ghi chú thành công"}

    def get_notes_by_user(self, user_id: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy danh sách ghi chú theo user_id."""
        notes = self.note_repo.get_notes_by_user(user_id, skip, limit)
        return [self._process_dynamic_status(note) for note in notes]

    def get_note_by_id(self, note_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Lấy ghi chú theo ID và kiểm tra quyền sở hữu."""
        note = self.note_repo.get_note_by_id(note_id)
        if not note or note.get("user_id") != user_id:
            return None 
        return self._process_dynamic_status(note)
        
    def search_notes_by_user(self, user_id: str, keyword: str, skip: int, limit: int) -> List[Dict[str, Any]]:
        """Tìm kiếm ghi chú của user theo từ khóa."""
        notes = self.note_repo.search_notes_by_user(user_id, keyword, skip, limit)
        return [self._process_dynamic_status(note) for note in notes]

    def update_note(self, note_id: str, note_data: NoteCreateSchema, user_id: str) -> Dict[str, Any]:
        """Cập nhật nội dung ghi chú."""
        existing_note = self.get_note_by_id(note_id, user_id)
        if not existing_note:
            raise ValueError("Ghi chú không tồn tại hoặc bạn không có quyền sửa")

        update_data = note_data.model_dump(exclude_unset=True)
        if not update_data:
            return {"message": "Không có dữ liệu để cập nhật"}

        self.note_repo.update_note(note_id, update_data)
        return {"id": note_id, "message": "Cập nhật ghi chú thành công"}

    def delete_note(self, note_id: str, user_id: str) -> Dict[str, Any]:
        """Xóa ghi chú theo ID."""
        existing_note = self.get_note_by_id(note_id, user_id)
        if not existing_note:
            raise ValueError("Ghi chú không tồn tại hoặc bạn không có quyền xóa")

        self.note_repo.delete_note(note_id)
        return {"id": note_id, "message": "Xóa ghi chú thành công"}

    def get_note_counts_by_date(self, user_id: str, period: str = "day") -> List[Dict[str, Any]]:
        """Thống kê số lượng ghi chú theo mốc thời gian."""
        return self.note_repo.get_note_counts_by_date(user_id, period)

    def get_note_counts_by_category(self, user_id: str) -> List[Dict[str, Any]]:
        """Thống kê số lượng ghi chú theo danh mục của user."""
        return self.note_repo.get_note_counts_by_category(user_id)

    def get_note_counts_by_status(self, user_id: str) -> List[Dict[str, Any]]:
        """Thống kê ghi chú theo trạng thái."""
        return self.note_repo.get_note_counts_by_status(user_id)