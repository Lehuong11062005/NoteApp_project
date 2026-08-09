from app.config.database import get_database
from datetime import datetime
from typing import Optional, Dict, Any
from bson.objectid import ObjectId


class NoteRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["notes"]

    @staticmethod
    def _to_object_id(note_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(note_id)
        except Exception:
            return None

    def create_note(self, note_data: dict) -> str:
        result = self.collection.insert_one(note_data)
        return str(result.inserted_id)

    def get_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        obj_id = self._to_object_id(note_id)
        note = self.collection.find_one({"_id": obj_id}) if obj_id else None
        if note:
            note["_id"] = str(note["_id"])
            if note.get("create_at") is not None:
                note["create_at"] = note["create_at"].isoformat()
            if note.get("update_at") is not None:
                note["update_at"] = note["update_at"].isoformat()
        return note

    def get_notes_by_user(self, user_id: str) -> list:
        cursor = self.collection.find({"user_id": user_id})
        notes = []
        for item in cursor:
            item["_id"] = str(item["_id"])
            if item.get("create_at") is not None:
                item["create_at"] = item["create_at"].isoformat()
            if item.get("update_at") is not None:
                item["update_at"] = item["update_at"].isoformat()
            notes.append(item)
        return notes

    def get_note_counts_by_date(self, user_id: str, period: str = "day") -> list:
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

    def update_note(self, note_id: str, update_data: dict):
        if "update_at" not in update_data:
            update_data["update_at"] = datetime.now()
        obj_id = self._to_object_id(note_id)
        result = self.collection.update_one({"_id": obj_id}, {"$set": update_data}) if obj_id else None
        return result.modified_count if result is not None else 0

    def delete_note(self, note_id: str):
        obj_id = self._to_object_id(note_id)
        result = self.collection.delete_one({"_id": obj_id}) if obj_id else None
        return result.deleted_count if result is not None else 0
