from app.config.database import get_database
from datetime import datetime
from typing import Optional, Dict, Any
from bson.objectid import ObjectId


class UserRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["users"]

    @staticmethod
    def _to_object_id(user_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(user_id)
        except Exception:
            return None

    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        obj_id = self._to_object_id(user_id)
        user = self.collection.find_one({"_id": obj_id}) if obj_id else None
        if user:
            user["_id"] = str(user["_id"])
            if user.get("created_at") is not None:
                user["created_at"] = user["created_at"].isoformat()
        return user

    def find_by_username(self, username: str):
        return self.collection.find_one({"username": username})

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def get_all_users(self) -> list:
        users = []
        for item in self.collection.find():
            item["_id"] = str(item["_id"])
            if item.get("created_at") is not None:
                item["created_at"] = item["created_at"].isoformat()
            users.append(item)
        return users

    def update_user(self, user_id: str, update_data: dict):
        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.now()
        obj_id = self._to_object_id(user_id)
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data}) if obj_id else None
        return result.modified_count if result is not None else 0

    def delete_user(self, user_id: str):
        obj_id = self._to_object_id(user_id)
        result = self.collection.delete_one({"_id": obj_id}) if obj_id else None
        return result.deleted_count if result is not None else 0