from app.config.database import get_database, close_database

class NoteRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["notes"]

    def create_note(self, note_data: dict) -> str:
        result = self.collection.insert_one(note_data)
        return str(result.inserted_id)

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
