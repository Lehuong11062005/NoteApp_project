from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends
from pymongo.database import Database
from app.config.database import get_database


class NoteRepository:
    def __init__(self, db: Database = Depends(get_database)):
        self.collection = db["notes"]

    @staticmethod
    def _to_object_id(note_id: str) -> Optional[ObjectId]:
        """Chuyển đổi string id sang ObjectId an toàn."""
        try:
            return ObjectId(note_id)
        except InvalidId:
            return None

    @staticmethod
    def _format_note(note: Dict[str, Any]) -> Dict[str, Any]:
        """Chuẩn hóa dữ liệu note trả về: ép kiểu _id và datetime sang string."""
        if not note:
            return note
        
        note["_id"] = str(note["_id"])
        
        for field in ["create_at", "update_at", "reminder_time"]:
            if note.get(field) and isinstance(note[field], datetime):
                note[field] = note[field].isoformat()
                
        return note

    def create_note(self, note_data: dict) -> str:
        """Tạo mới một note."""
        if "create_at" not in note_data:
            note_data["create_at"] = datetime.now(timezone.utc)
            
        result = self.collection.insert_one(note_data)
        return str(result.inserted_id)

    def get_notes_by_user(self, user_id: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy danh sách note theo user_id có phân trang, hỗ trợ cả String và ObjectId."""
        
        # 1. Mặc định tìm theo kiểu String
        query_conditions = [{"user_id": user_id}]
        
        # 2. Nếu user_id có thể ép kiểu sang ObjectId, tìm thêm cả kiểu ObjectId
        obj_id = self._to_object_id(user_id)
        if obj_id:
            query_conditions.append({"user_id": obj_id})
            
        # Gom điều kiện lại bằng $or (tìm thấy 1 trong 2 kiểu là lấy)
        query = {"$or": query_conditions}

        cursor = self.collection.find(query).skip(skip).limit(limit)
        return [self._format_note(item) for item in cursor]

    def get_notes_by_user(self, user_id: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy danh sách note theo user_id có phân trang."""
        cursor = self.collection.find({"user_id": user_id}).skip(skip).limit(limit)
        return [self._format_note(item) for item in cursor]

    def search_notes_by_user(self, user_id: str, keyword: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Tìm kiếm note của user theo từ khóa có phân trang."""
        normalized_keyword = (keyword or "").strip()
        query: Dict[str, Any] = {"user_id": user_id}
        
        if normalized_keyword:
            query["$or"] = [
                {"title": {"$regex": normalized_keyword, "$options": "i"}},
                {"content": {"$regex": normalized_keyword, "$options": "i"}},
                {"category": {"$regex": normalized_keyword, "$options": "i"}},
                {"priority": {"$regex": normalized_keyword, "$options": "i"}},
            ]

        cursor = self.collection.find(query).skip(skip).limit(limit)
        return [self._format_note(item) for item in cursor]

    def update_note(self, note_id: str, update_data: dict) -> bool:
        """Cập nhật thông tin note."""
        obj_id = self._to_object_id(note_id)
        if not obj_id:
            return False

        update_data["update_at"] = datetime.now(timezone.utc)
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_note(self, note_id: str) -> bool:
        """Xóa note theo ID."""
        obj_id = self._to_object_id(note_id)
        if not obj_id:
            return False

        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0

    def get_note_counts_by_date(self, user_id: str, period: str = "day") -> List[Dict[str, Any]]:
        """Thống kê số lượng ghi chú theo thời gian (ngày hoặc tháng)."""
        date_format = "%Y-%m" if period == "month" else "%Y-%m-%d"
        pipeline = [
            {"$match": {"user_id": user_id, "create_at": {"$exists": True}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": date_format,
                            "date": "$create_at",
                        }
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        return [
            {"date": item["_id"], "count": item["count"]}
            for item in self.collection.aggregate(pipeline)
        ]

    def get_note_counts_by_category(self, user_id: str) -> List[Dict[str, Any]]:
        """Thống kê số lượng ghi chú theo danh mục của user."""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": {"$ifNull": ["$category", "Chung"]},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1, "_id": 1}},
        ]
        return [
            {"category": item["_id"], "count": item["count"]}
            for item in self.collection.aggregate(pipeline)
        ]

    def get_note_counts_by_status(self, user_id: str) -> List[Dict[str, Any]]:
        """Thống kê số lượng ghi chú theo trạng thái."""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": {"$ifNull": ["$status", "Đang chờ"]}, 
                "count": {"$sum": 1}
            }}
        ]
        return [
            {"status": item["_id"], "count": item["count"]} 
            for item in self.collection.aggregate(pipeline)
        ]