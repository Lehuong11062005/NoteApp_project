from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends
from pymongo.database import Database
from app.config.database import get_database


class NotificationRepository:
    def __init__(self, db: Database = Depends(get_database)):
        self.collection = db["notifications"]

    @staticmethod
    def _to_object_id(notif_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(notif_id)
        except InvalidId:
            return None

    @staticmethod
    def _format_notification(item: Dict[str, Any]) -> Dict[str, Any]:
        if not item:
            return item
        item["id"] = str(item["_id"])
        item["_id"] = str(item["_id"])
        for field in ["created_at", "read_at"]:
            if item.get(field) and isinstance(item[field], datetime):
                item[field] = item[field].isoformat()
        return item

    def create_notification(self, data: dict) -> str:
        if "created_at" not in data:
            data["created_at"] = datetime.now(timezone.utc)
        if "is_read" not in data:
            data["is_read"] = False
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get_by_user(self, user_id: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        return [self._format_notification(item) for item in cursor]

    def count_unread(self, user_id: str) -> int:
        return self.collection.count_documents({"user_id": user_id, "is_read": False})

    def mark_as_read(self, notif_id: str, user_id: str) -> bool:
        obj_id = self._to_object_id(notif_id)
        if not obj_id:
            return False
        result = self.collection.update_one(
            {"_id": obj_id, "user_id": user_id},
            {"$set": {"is_read": True, "read_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count > 0

    def mark_all_as_read(self, user_id: str) -> int:
        result = self.collection.update_many(
            {"user_id": user_id, "is_read": False},
            {"$set": {"is_read": True, "read_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count

    def delete(self, notif_id: str, user_id: str) -> bool:
        obj_id = self._to_object_id(notif_id)
        if not obj_id:
            return False
        result = self.collection.delete_one({"_id": obj_id, "user_id": user_id})
        return result.deleted_count > 0

    def delete_all(self, user_id: str) -> int:
        result = self.collection.delete_many({"user_id": user_id})
        return result.deleted_count
