from app.config.database import get_database
from datetime import datetime
from typing import Optional, Dict, Any
from bson.objectid import ObjectId


class CategoryRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["categories"]

    @staticmethod
    def _to_object_id(category_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(category_id)
        except Exception:
            return None

    def create_category(self, category_data: dict) -> str:
        result = self.collection.insert_one(category_data)
        return str(result.inserted_id)

    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        obj_id = self._to_object_id(category_id)
        category = self.collection.find_one({"_id": obj_id}) if obj_id else None
        if category:
            category["_id"] = str(category["_id"])
            if category.get("created_at") is not None:
                category["created_at"] = category["created_at"].isoformat()
            if category.get("updated_at") is not None:
                category["updated_at"] = category["updated_at"].isoformat()
        return category

    def get_all_categories(self) -> list:
        categories = []
        for item in self.collection.find():
            item["_id"] = str(item["_id"])
            if item.get("created_at") is not None:
                item["created_at"] = item["created_at"].isoformat()
            if item.get("updated_at") is not None:
                item["updated_at"] = item["updated_at"].isoformat()
            categories.append(item)
        return categories

    def update_category(self, category_id: str, update_data: dict):
        if "updated_at" not in update_data:
            update_data["updated_at"] = datetime.now()
        obj_id = self._to_object_id(category_id)
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data}) if obj_id else None
        return result.modified_count if result is not None else 0

    def delete_category(self, category_id: str):
        obj_id = self._to_object_id(category_id)
        result = self.collection.delete_one({"_id": obj_id}) if obj_id else None
        return result.deleted_count if result is not None else 0
