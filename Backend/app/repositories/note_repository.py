from app.config.database import get_database, close_database

class NoteRepository:
    def __init__(self):
        self.db=get_database()
        self.collection=self.db["notes"]

    def create_note(self, note_data:dict) ->str:
        result=self.collection.insert_one(note_data)
        return str(result.inserted_id)
    
