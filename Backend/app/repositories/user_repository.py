from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.database import Database
from fastapi import Depends
from app.config.database import get_database

class UserRepository:
    def __init__(self, db: Database = Depends(get_database)):
        self.collection = db["users"]

    @staticmethod
    def _to_object_id(user_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(user_id)
        except InvalidId:
            return None

    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        obj_id = self._to_object_id(user_id)
        if not obj_id:
            return None
            
        user = self.collection.find_one({"_id": obj_id})
        if user:
            user["_id"] = str(user["_id"])
            if user.get("created_at"):
                user["created_at"] = user["created_at"].isoformat()
        return user

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"username": username})

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({"email": email})

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        users = []
        cursor = self.collection.find().skip(skip).limit(limit)
        for item in cursor:
            item["_id"] = str(item["_id"])
            if item.get("created_at"):
                item["created_at"] = item["created_at"].isoformat()
            users.append(item)
        return users

    def update_user(self, user_id: str, update_data: dict) -> int:
        obj_id = self._to_object_id(user_id)
        if not obj_id:
            return 0
            
        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data})
        return result.modified_count

    def delete_user(self, user_id: str) -> int:
        obj_id = self._to_object_id(user_id)
        if not obj_id:
            return 0
            
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count