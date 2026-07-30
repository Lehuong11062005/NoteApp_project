from bson import ObjectId
from app.config.database import get_database, close_database

class NoteRepository:
    def __init__(self):
        self.db=get_database()
        self.collection=self.db["notes"]

    def create_note(self, note_data:dict) ->str:
        result=self.collection.insert_one(note_data)
        return str(result.inserted_id)

    def update_note(self, note_id:str, note_data:dict) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": note_data}
        )
        return result.modified_count > 0

    def get_all_notes(self):
        notes = list(self.collection.find())
        for note in notes:
            note["_id"] = str(note["_id"])
        return notes

