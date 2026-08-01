from app.config.database import get_database
from datetime import datetime
from typing import Optional, Dict, Any
from bson.objectid import ObjectId


class ReminderRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["reminders"]

    @staticmethod
    def _to_object_id(reminder_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(reminder_id)
        except Exception:
            return None

    def create_reminder(self, reminder_data: dict) -> str:
        result = self.collection.insert_one(reminder_data)
        return str(result.inserted_id)

    def get_reminder_by_id(self, reminder_id: str) -> Optional[Dict[str, Any]]:
        obj_id = self._to_object_id(reminder_id)
        reminder = self.collection.find_one({"_id": obj_id}) if obj_id else None
        if reminder:
            reminder["_id"] = str(reminder["_id"])
            if reminder.get("created_at") is not None:
                reminder["created_at"] = reminder["created_at"].isoformat()
            if reminder.get("updated_at") is not None:
                reminder["updated_at"] = reminder["updated_at"].isoformat()
        return reminder

    def get_reminders_by_user(self, user_id: str) -> list:
        reminders = []
        cursor = self.collection.find({"user_id": user_id})
        for item in cursor:
            item["_id"] = str(item["_id"])
            if item.get("created_at") is not None:
                item["created_at"] = item["created_at"].isoformat()
            if item.get("updated_at") is not None:
                item["updated_at"] = item["updated_at"].isoformat()
            reminders.append(item)
        return reminders

    def update_reminder(self, reminder_id: str, update_data: dict):
        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.now()
        obj_id = self._to_object_id(reminder_id)
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data}) if obj_id else None
        return result.modified_count if result is not None else 0

    def delete_reminder(self, reminder_id: str):
        obj_id = self._to_object_id(reminder_id)
        result = self.collection.delete_one({"_id": obj_id}) if obj_id else None
        return result.deleted_count if result is not None else 0
